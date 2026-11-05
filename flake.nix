{
  description = "Petri nets for IMS (FIT VUT): diagrams, note PDFs, SIMLIB models";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAll = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      packages = forAll (pkgs: rec {
        # SIMLIB/C++ (Peringer, FIT VUT) is not in nixpkgs; built from the official source.
        simlib = pkgs.stdenv.mkDerivation {
          pname = "simlib";
          version = "3.10-20260914";
          src = pkgs.fetchurl {
            url = "https://www.fit.vut.cz/person/peringer/public/SIMLIB/source/simlib-3.10-20260914.tar.gz";
            hash = "sha256-jmbHyRilioTIoVBALPZGCZz7NkYAgKyTBKR1uPgqvDs=";
          };
          # the library's makefiles call `gmake`
          preBuild = ''
            mkdir -p "$TMPDIR/bin"
            ln -s "$(command -v make)" "$TMPDIR/bin/gmake"
            export PATH="$TMPDIR/bin:$PATH"
          '';
          buildPhase = ''
            runHook preBuild
            make -C src
            runHook postBuild
          '';
          installPhase = ''
            runHook preInstall
            make -C src install PREFIX=$out
            runHook postInstall
          '';
          meta = {
            description = "SIMulation LIBrary for C++";
            homepage = "https://www.fit.vut.cz/person/peringer/public/SIMLIB/";
            license = pkgs.lib.licenses.lgpl2Plus;
          };
        };
        default = simlib;
      });

      devShells = forAll (pkgs:
        let
          tex = pkgs.texliveSmall.withPackages (ps: with ps; [
            # diagrams (TikZ)
            pgf lm
            # note PDFs (pandoc's LaTeX template with xelatex)
            babel-czech fontspec unicode-math xcolor hyperref bookmark geometry
            booktabs etoolbox fancyvrb framed upquote microtype xurl footnotehyper
            parskip lineno
            # long code lines wrap instead of running off the page
            fvextra
            # textbook look (pn/note-style.tex)
            titlesec tcolorbox tikzfill pdfcol enumitem caption fancyhdr newunicodechar
          ]);
        in
        {
          default = pkgs.mkShell {
            packages = [
              pkgs.python3
              tex
              pkgs.poppler-utils # pdftocairo, pdftoppm
              pkgs.pandoc
              pkgs.gnumake
              self.packages.${pkgs.stdenv.hostPlatform.system}.simlib
            ];
            # xelatex finds the Latin Modern fonts by file name in TeX Live; fontconfig only needs
            # to exist, independent of the system
            FONTCONFIG_FILE = pkgs.makeFontsConf { fontDirectories = [ ]; };
          };
        });
    };
}
