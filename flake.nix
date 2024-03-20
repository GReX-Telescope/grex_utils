{
  description = "GReX Utils Python Library Dev Environment";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      overlays = [ ];
      pkgs = import nixpkgs {inherit system overlays;};
      nativeBuildInputs = [];
      buildInputs =
        with pkgs; [
          # Python requirements
          python3
          poetry

          # Linting support
          codespell
          alejandra
        ];
    in
      with pkgs; {
        devShells.default = mkShell {inherit buildInputs nativeBuildInputs;};
      });
}
