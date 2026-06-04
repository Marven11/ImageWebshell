{
  description = "Image webshell generator";

  inputs = {
    utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
  };

  outputs =
    { self
    , nixpkgs
    , utils
    , ...
    }:
    utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
      pythonPackages = pkgs.python3Packages;
    in
    {
      devShells.default = pkgs.mkShell {
        name = "image-webshell";
        venvDir = "./.venv";
        buildInputs = with pythonPackages; [
          python
          venvShellHook
          pillow
          fire
          numpy
        ];
        postVenvCreation = ''
          unset SOURCE_DATE_EPOCH
        '';
        postShellHook = ''
          unset SOURCE_DATE_EPOCH
        '';
      };

      packages.default = with pythonPackages; buildPythonApplication {
        pname = "image-webshell";
        version = "0.0.3";
        doCheck = false;

        build-system = [
          setuptools
          setuptools-scm
        ];

        dependencies = [
          pillow
          fire
          numpy
        ];
        src = ./.;
      };
    });
}
