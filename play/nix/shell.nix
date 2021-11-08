# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

with import <nixpkgs> {};

stdenv.mkDerivation rec {
  name = "materialize";
  buildInputs = with pkgs; [
      cmake
      rustup
      openssl
      pkg-config
      lld_13
      python38Packages.pip
    ];

  hardeningDisable = [ "fortify" ];

  MZ_DEV = 1;
  RUSTFLAGS = "-C link-arg=-fuse-ld=lld -C debuginfo=1";
  shellHook = ''
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:${lib.makeLibraryPath buildInputs}"
   '';
}
