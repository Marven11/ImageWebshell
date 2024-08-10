{
  description = "Python venv development template";

  inputs = {
    utils.url = "github:numtide/flake-utils";
    nixpkgsOld.url = "https://github.com/NixOS/nixpkgs/archive/b4e193a23a1c5d8794794e65cabf1f1135d07fd9.tar.gz";
  };

  outputs =
    { self
    , nixpkgs
    , nixpkgsOld
    , utils
    , ...
    }:
    utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
      pkgsOld = import nixpkgsOld { inherit system; };
      pythonPackages = pkgs.python3Packages;
      python37Packages = pkgsOld.python37Packages;
    in
    {
      devShells.default = pkgs.mkShell {
        name = "python-venv";
        venvDir = "./.venv";
        buildInputs = with pythonPackages; [
          python
          venvShellHook
          notebook
          ipython
          pillow
          fire
          numpy
        ];
        postVenvCreation = ''
          unset SOURCE_DATE_EPOCH
          pip install -r requirements.txt
        '';
        postShellHook = ''
          # allow pip to install wheels
          unset SOURCE_DATE_EPOCH
        '';
      };

      packages.default = with pythonPackages; buildPythonApplication {
        pname = "image-webshell";
        version = "0.0.2";
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
