MKVToolNix 66.0.0
=================

# Table of contents

1. [Introduction](#1-introduction)
2. [Installation](#2-installation)
    1. [Requirements](#21-requirements)
        1. [Hard requirements](#211-hard-requirements)
        2. [Requirements with bundled fallbacks](#212-requirements-with-bundled-fallbacks)
    2. [Optional components](#22-optional-components)
    3. [Building libEBML and libMatroska](#23-building-libebml-and-libmatroska)
    4. [Building MKVToolNix](#24-building-mkvtoolnix)
        1. [Getting and building a development snapshot](#241-getting-and-building-a-development-snapshot)
        2. [Configuration and compilation](#242-configuration-and-compilation)
    5. [Notes for compilation on (Open)Solaris](#25-notes-for-compilation-on-opensolaris)
    6. [Unit tests](#26-unit-tests)
3. [Reporting bugs & getting support](#3-reporting-bugs-getting-support)
    1. [Reporting bugs](#31-reporting-bugs)
    2. [Getting support](#32-getting-support)
4. [Test suite and continuous integration tests](#4-test-suite-and-continuous-integration-tests)
5. [Code of Conduct](#5-code-of-conduct)
6. [Included third-party components and their licenses](#6-included-third-party-components-and-their-licenses)
    1. [avilib](#61-avilib)
    2. [libEBML](#63-libebml)
    3. [libMatroska](#64-libmatroska)
    4. [librmff](#65-librmff)
    5. [nlohmann's JSON](#66-nlohmanns-json)
    6. [pugixml](#67-pugixml)
    7. [utf8-cpp](#68-utf8-cpp)
    8. [Oxygen icons and sound files](#69-oxygen-icons-and-sound-files)
    9. [MKVToolNix icons](#610-mkvtoolnix-icons)
    10. [QtWaitingSpinner](#611-qtwaitingspinner)
    11. [Fancy tab widget](#612-fancy-tab-widget)
    12. [fmt](#613-fmt)

-----------------

# 1. Introduction

With these tools one can get information about (via mkvinfo) Matroska
files, extract tracks/data from (via mkvextract) Matroska files and create
(via mkvmerge) Matroska files from other media files. Matroska is a new
multimedia file format aiming to become THE new container format for
the future. You can find more information about it and its underlying
technology, the Extensible Binary Meta Language (EBML), at

http://www.matroska.org/

The full documentation for each command is now maintained in its
man page only. Type `mkvmerge -h` to get you started.

This code comes under the GPL v2 (see www.gnu.org or the file COPYING).
Modify as needed.

The icons are based on the work of Alexandr Grigorcea and modified by
Eduard Geier. They're licensed under the terms of the
[Creative Commons Attribution 3.0 Unported license](http://creativecommons.org/licenses/by/3.0/).

The newest version can always be found at
https://mkvtoolnix.download/

Moritz Bunkus <moritz@bunkus.org>


# 2. Installation

If you want to compile the tools yourself, you must first decide
if you want to use a 'proper' release version or the current
development version. As both Matroska and MKVToolNix are under heavy
development, there might be features available in the git repository
that are not available in the releases. On the other hand the git
repository version might not even compile.

## 2.1. Requirements

### 2.1.1. Hard requirements

In order to compile MKVToolNix, you need a couple of libraries. Most of
them should be available pre-compiled for your distribution. The
programs and libraries you absolutely need are:

- A C++ compiler that supports several features of the C++11, C++14
  and C++17 standards: initializer lists, range-based `for` loops,
  right angle brackets, the `auto` keyword, lambda functions, the
  `nullptr` keyword, tuples, alias declarations, `std::make_unique()`,
  digit separators, binary literals, generic lambdas, user-defined
  literals for `std::string`, `[[maybe_unused]]` attribute, nested
  namespace definition, structured bindings, `std::optional`,
  `std::regex`. Others may be needed, too. For GCC this means at least
  v8; for clang v7 or later.

- [libOgg](http://downloads.xiph.org/releases/ogg/) and
  [libVorbis](http://downloads.xiph.org/releases/vorbis/) for access to Ogg/OGM
  files and Vorbis support

- [zlib](http://www.zlib.net/) — a compression library

- [Boost](http://www.boost.org/) — Several of Boost's libraries are
  used, e.g. `operators`, `multi-precision`. At least v1.66.0 is required.

- [libxslt's xsltproc binary](http://xmlsoft.org/libxslt/) and
  [DocBook XSL stylesheets](https://sourceforge.net/projects/docbook/files/docbook-xsl/)
  — for creating man pages from XML documents

You also need the `rake` or `drake` build program. I suggest `rake`
v10.0.0 or newer (this is included with Ruby 2.1) as it offers
parallel builds out of the box. If you only have an earlier version of
`rake`, you can install and use the `drake` gem for the same gain.

### 2.1.2. Requirements with bundled fallbacks

Several required libraries might not be available for your
distribution. Therefore they're bundled with the MKVToolNix source
code. The `configure` script will look for those libraries and use
existing versions if present. If not, the bundled versions are used
instead.

It is highly recommended to install the versions provided by your
distribution instead of relying on the bundled versions.

These libraries are:

- [fmt](http://fmtlib.net/) — a small, safe and fast formatting
  library. Version 6.1.0 or later is required.

- [libEBML v1.4.2](http://dl.matroska.org/downloads/libebml/) or later
  and [libMatroska v1.6.3](http://dl.matroska.org/downloads/libmatroska/)
  or later for low-level access to Matroska files. Instructions on how to
  compile them are a bit further down in this file.

- [librmff](https://www.bunkus.org/videotools/librmff/index.html) — a
  library for accessing RealMedia files

- [nlohmann's JSON](https://github.com/nlohmann/json) — JSON for
  Modern C++

- [Qt](http://www.qt.io/) v5.9.0 or newer — a cross-platform library
  including a UI toolkit. The library is needed for all programs, even
  if you decide not to build MKVToolNix GUI.

- [pugixml](http://pugixml.org/) — light-weight, simple and fast XML
  parser for C++ with XPath support

- [utf8-cpp](http://utfcpp.sourceforge.net/) — UTF-8 with C++ in a
  Portable Way

## 2.2. Optional components

Other libraries are optional and only limit the features that are
built. These include:

- [cmark](https://github.com/commonmark/cmark) — the CommonMark
  parsing and rendering library in C is required when building
  MKVToolNix GUI.

- [libFLAC](http://downloads.xiph.org/releases/flac/) for FLAC
  support (Free Lossless Audio Codec)

- [po4a](https://po4a.alioth.debian.org/) for building the translated
  man pages

## 2.3. Building libEBML and libMatroska

This is optional as MKVToolNix comes with its own set of the
libraries. It will use them if no version is found on the system.

Start by either downloading the latest releases of
[libEBML](http://dl.matroska.org/downloads/libebml/) and
[libMatroska](http://dl.matroska.org/downloads/libmatroska/) or by
getting fresh copies from their git repositories:

    git clone https://github.com/Matroska-Org/libebml.git
    git clone https://github.com/Matroska-Org/libmatroska.git

First build and install libEBML according to the included
instructions. Afterwards do the same for libMatroska.

## 2.4. Building MKVToolNix

Either download the current release from
[the MKVToolNix home page](https://mkvtoolnix.download/)
and unpack it or get a development snapshot from my Git repository.

### 2.4.1. Getting and building a development snapshot

You can ignore this subsection if you want to build from a release
tarball.

All you need for Git repository access is to download a Git client
from the Git homepage at http://git-scm.com/. There are clients
for both Unix/Linux and Windows.

First clone my Git repository with this command:

    git clone https://gitlab.com/mbunkus/mkvtoolnix.git

Now change to the MKVToolNix directory with `cd mkvtoolnix` and run
`./autogen.sh` which will generate the "configure" script. You need
the GNU "autoconf" utility for this step.

### 2.4.2. Configuration and compilation

If you have run `make install` for both libraries, then `configure`
should automatically find the libraries' position. Otherwise you need
to tell `configure` where the libEBML and libMatroska include and
library files are:

    ./configure \
      --with-extra-includes=/where/i/put/libebml\;/where/i/put/libmatroska \
      --with-extra-libs=/where/i/put/libebml/make/linux\;/where/i/put/libmatroska/make/linux

Now run `rake` and, as "root", `rake install`.

### 2.4.3. If things go wrong

By default the commands executed by the build system aren't
output. You can change that by adding `V=1` as an argument to the
`rake` command.

If `rake` executes too many processes at once, then you've stumbled
across a known bug in `rake`. In that case you should install the
`drake` Ruby gem and use the command `drake` instead of
`rake`. `drake` supports parallelism properly and doesn't try to
execute all jobs at once.

## 2.5. Notes for compilation on (Open)Solaris

You can compile MKVToolNix with Sun's sunstudio compiler, but you need
additional options for `configure`:

    ./configure --prefix=/usr \
      CXX="/opt/sunstudio12.1/bin/CC -library=stlport4" \
      CXXFLAGS="-D_POSIX_PTHREAD_SEMANTICS" \
      --with-extra-includes=/where/i/put/libebml\;/where/i/put/libmatroska \
      --with-extra-libs=/where/i/put/libebml/make/linux\;/where/i/put/libmatroska/make/linux

## 2.6. Unit tests

Building and running unit tests is completely optional. If you want to
do this, you have to follow these steps:

1. Download the "googletest" framework from
   https://github.com/google/googletest/ (at the time of writing the
   file to download was "googletest-release-1.8.0.tar.gz")

2. Extract the archive somewhere and create a symbolic link to its
   `googletest-release-1.8.0/googletest` sub-directory
   inside MKVToolNix' `lib` directory and call it `gtest`, e.g. like this:

   `ln -s /path/to/googletest-release-1.8.0/googletest lib/gtest`

3. Configure MKVToolNix normally.

4. Build the unit test executable and run it with

        rake tests:run_unit


# 3. Reporting bugs & getting support

# 3.1. Reporting bugs

If you're sure you've found a bug — e.g. if one of my programs crashes
with an obscur error message, or if the resulting file is missing part
of the original data, then by all means submit a bug report.

I use [GitLab's issue system](https://gitlab.com/mbunkus/mkvtoolnix/issues)
as my bug database. You can submit your bug reports there. Please be as
verbose as possible — e.g. include the command line, if you use Windows
or Linux etc.pp.

If at all possible, please include sample files as well so that I can
reproduce the issue. If they are larger than 1 MB, please upload
them somewhere and post a link in the issue. You can also upload them
to my FTP server. Details on how to connect can be found in the
[MKVToolNix FAQ](https://gitlab.com/mbunkus/mkvtoolnix/wikis/FTP-server).

# 3.2. Getting support

The issue tracker above is not meant for general support which you can
find in the following places:

* The [MKVToolNix sub-Reddit](https://www.reddit.com/r/mkvtoolnix) is
  suitable for all kinds of questions.
* The MKVToolNix thread on [Doom9's
  forum](http://forum.doom9.org/showthread.php?t=155732) is more
  suited for in-depth technical questions.
* There's also the IRC channel `#matroska` on the [Freenode IRC
  network](https://freenode.net/) where we hang out. The main
  MKVToolNix author Moritz Bunkus is known as "mosu" there.


# 4. Test suite and continuous integration tests

MKVToolNix contains a lot of test cases in order to detect regressions
before they're released. Regressions include both compilation issues
as well as changes from expected program behavior.

As mentioned in section 2.6., MKVToolNix comes with a set of unit
tests based on the Google Test library in the `tests/unit`
sub-directory that you can run yourself. These cover only a small
amount of code, and any effort to extend them would be most welcome.

A second test suite exists that targets the program behavior, e.g. the
output generated by mkvmerge when specific options are used with
specific input files. These are the test cases in the `tests`
directory itself. Unfortunately the files they run on often contain
copyrighted material that I cannot distribute. Therefore you cannot
run them yourself.

A third pillar of the testing effort is the
[continuous integration tests](https://buildbot.mkvtoolnix.download/)
run on a Buildbot instance. These are run automatically for each
commit made to the git repository. The tests include:

  * building of all the packages for Linux distributions that I
    normally provide for download myself in both 32-bit and 64-bit
    variants
  * building of the Windows installer and portable packages in both
    32-bit and 64-bit variants
  * building with both g++ and clang++
  * building and running the unit tests
  * building and running the test file test suite
  * building with all optional features disabled

# 5. Code of Conduct

Please note that this project is released with a
[Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project
you agree to abide by its terms.

# 6. Included third-party components and their licenses

MKVToolNix includes and uses the following libraries & artwork:

## 6.1. avilib

Reading and writing AVI files. Originally part of the `transcode`
package.

  * Copyright: 1999 Rainer Johanni <Rainer@Johanni.de>
  * License: GNU General Public License v2 or later
  * URL: the `transcode` project doesn't seem to have a home page anymore
  * Corresponding files: `lib/avilib-0.6.10/*`

## 6.2. libEBML

A C++ library to parse EBML files

  * Copyright: 2002-2021 Steve Lhomme et. al.
  * License: GNU Lesser General Public License v2.1 or later (see `doc/licenses/LGPL-2.1.txt`)
  * URL: http://www.matroska.org/
  * Corresponding files: `lib/libebml/*`

## 6.3. libMatroska

A C++ library to parse Matroska files

  * Copyright: 2002-2020 Steve Lhomme et. al.
  * License: GNU Lesser General Public License v2.1 or later (see `doc/licenses/LGPL-2.1.txt`)
  * URL: http://www.matroska.org/
  * Corresponding files: `lib/libmatroska/*`

## 6.4. librmff

librmff is short for 'RealMedia file format access library'. It aims
at providing the programmer an easy way to read and write RealMedia
files.

  * Copyright: Moritz Bunkus
  * License: GNU Lesser General Public License v2.1 or later (see `doc/licenses/LGPL-2.1.txt`)
  * URL: https://www.bunkus.org/videotools/librmff/index.html
  * Corresponding files: `lib/librmff/*`

## 6.5. nlohmann's JSON

JSON for Modern C++

  * Copyright: 2013-2021 Niels Lohmann
  * License: MIT (see `doc/licenses/nlohmann-json-MIT.txt`)
  * URL: https://github.com/nlohmann/json
  * Corresponding files: `lib/nlohmann-json/*`

## 6.6. pugixml

An XML processing library

  * Copyright: 2006–2020 by Arseny Kapoulkine <arseny.kapoulkine@gmail.com>
  * License: MIT (see `doc/licenses/pugixml-MIT.txt`)
  * URL: https://pugixml.org/
  * Corresponding files: `lib/pugixml/*`

## 6.7. utf8-cpp

UTF-8 with C++ in a Portable Way

  * Copyright: 2006-2021 Nemanja Trifunovic
  * License: Boost Software License 1.0 (see `doc/licenses/Boost-1.0.txt`)
  * URL: https://github.com/nemtrif/utfcpp/
  * Corresponding files: `lib/utf8-cpp/*`

## 6.8. Oxygen icons and sound files

Most of the icons included in this package originate from the Oxygen
Project. These include all files in the `share/icons` sub-directory
safe for those whose name starts with `mkv`.

The preferred form of modification are the SVG icons. These are not
part of the binary distribution of MKVToolNix, but they are contained
in the source code in the `icons/scalable` sub-directory. You can
obtain the source code from the
[MKVToolNix website](https://mkvtoolnix.download/).

All of the sound files in the `share/sounds` sub-directory originate
from the Oxygen project.

  * License: GNU Lesser General Public License v3 (see `doc/licenses/LGPL-3.0.txt`)
  * URL: https://techbase.kde.org/Projects/Oxygen
  * Corresponding files:
    * `share/icons/*` (except for `share/icons/*/mkv*`)
    * `share/sounds/*`

## 6.9. MKVToolNix icons

  * Copyright:
    * 2011 Alexandr Grigorcea <cahr.gr@gmail.com>
    * 2012 Eduard Geier <edu.g@online.de>
    * 2012 Ben Humpert <ben@an3k.de>
  * License: Creative Commons Attribution 3.0 Unported (CC BY 3.0) (see `doc/licenses/CC-BY-3.0.txt`)
  * Corresponding files: `share/icons/*/mkv*`

## 6.10. QtWaitingSpinner

A highly configurable, custom Qt widget for showing "waiting" or
"loading" spinner icons in Qt applications

  * Copyright:
    * 2012–2014 by Alexander Turkin
    * 2014 by William Hallatt
    * 2015 by Jacob Dawid
  * License: MIT (see `doc/licenses/QtWaitingSpinner-MIT.txt`)
  * URL: https://github.com/snowwlex/QtWaitingSpinner
  * Corresponding files: `src/mkvtoolnix-gui/util/waiting_spinning_widget.{h,cpp}`

## 6.11. Fancy tab widget

A beefed-up tab widget class for Qt extracted from the Qt Creator project

  * Copyright: 2011 Nokia Corporation and/or its subsidiary(-ies).
  * License: GNU General Public License v2 (see `COPYING`)
  * Corresponding files: `src/mkvtoolnix-gui/util/fancy_tab_widget.{h,cpp}`

## 6.12. fmt

Small, safe and fast formatting library

  * Copyright: 2012–present by Victor Zverovich
  * License: BSD (see `doc/licenses/fmt-BSD.txt`)
  * URL: http://fmtlib.net/latest/
  * Corresponding files: `lib/fmt/*`
