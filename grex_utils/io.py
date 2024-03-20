# Module for dealing with File IO of GReX data products
from typing import Optional

import xarray


def read_voltage_as_stokesi(
    file_name: str,
    time_downsample: Optional[int] = None,
    freq_downsample: Optional[int] = None,
    time_chunks: int = 2048,
) -> xarray.DataArray:
    """Read in the voltage data from a .nc file
    and return it as Stokes intensity.

    Parameters
    ----------
    file_name
        The file name of the .nc file with voltages
    time_downsample
        The factor to downsample in time
    freq_downsample
        The factor to downsample in frequency
    time_chunks
        The netcdf reader chunk size in the time dimension

    Returns
    -------
    stokesi
        The Stokes I data object
    """

    # Open the file and extract the voltages
    ds = xarray.open_dataset(file_name, chunks={"time": time_chunks})
    voltages = ds["voltages"]

    # Make Stokes I by converting to XX/YY and then creating XX**2 + YY**2
    # We need to first promote the complex components to int32 to deal with bitgrowth from square and summing
    # No need to create complex numbers and then find the abs, as that's an unnecessary sqrt
    stokesi = (
        voltages.sel(reim="real").astype("int32") ** 2
        + voltages.sel(reim="imaginary").astype("int32") ** 2
    ).sum(dim="pol")

    # These don't type check because of https://github.com/pydata/xarray/issues/8136
    if time_downsample is not None:
        stokesi = stokesi.coarsen(time=time_downsample, boundary="trim").mean()
    if freq_downsample is not None:
        stokesi = stokesi.coarsen(freq=freq_downsample, boundary="trim").mean()

    return stokesi
