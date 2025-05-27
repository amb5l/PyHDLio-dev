# Third-Party Licenses

This document lists all third-party projects and their licenses used in PyHDLio.

## Test Projects (Git Submodules)

The following VHDL projects are included as git submodules for testing purposes only. They are not distributed as part of PyHDLio and their inclusion does not affect PyHDLio's licensing.

### en_cl_fix
- **Repository**: https://github.com/enclustra/en_cl_fix
- **License**: MIT License
- **Usage**: Testing PyHDLio parser against professional fixed-point arithmetic library
- **Location**: `tests/projects/en_cl_fix/`

```
MIT License

Copyright (c) 2017 Enclustra GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### OSVVM (Open Source VHDL Verification Methodology)
- **Repository**: https://github.com/OSVVM/OSVVM
- **License**: Apache License 2.0
- **Usage**: Testing PyHDLio parser against industry-standard VHDL verification library
- **Location**: `tests/projects/osvvm/`

```
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions.

"License" shall mean the terms and conditions for use, reproduction,
and distribution as defined by Sections 1 through 9 of this document.

"Licensor" shall mean the copyright owner or entity granting the License.

"Legal Entity" shall mean the union of the acting entity and all
other entities that control, are controlled by, or are under common
control with that entity. For the purposes of this definition,
"control" means (i) the power, direct or indirect, to cause the
direction or management of such entity, whether by contract or
otherwise, or (ii) ownership of fifty percent (50%) or more of the
outstanding shares, or (iii) beneficial ownership of such entity.

"You" (or "Your") shall mean an individual or Legal Entity
exercising permissions granted by this License.

"Source" form shall mean the preferred form for making modifications,
including but not limited to source code, documentation, and
configuration files.

"Object" form shall mean any form resulting from mechanical
transformation or translation of a Source form, including but
not limited to compiled object code, generated documentation,
and conversions to other media types.

"Work" shall mean the work of authorship, whether in Source or
Object form, made available under the License, as indicated by a
copyright notice that is included in or attached to the work
(whether in Exhibits A, B or C as applicable).

"Derivative Works" shall mean any work, whether in Source or Object
form, that is based upon (or derived from) the Work and for which the
editorial revisions, annotations, elaborations, or other modifications
represent, as a whole, an original work of authorship. For the purposes
of this License, Derivative Works shall not include works that remain
separable from, or merely link (or bind by name) to the interfaces of,
the Work and derivative works thereof.

"Contribution" shall mean any work of authorship, including
the original version of the Work and any modifications or additions
to that Work or Derivative Works thereof, that is intentionally
submitted to Licensor for inclusion in the Work by the copyright owner
or by an individual or Legal Entity authorized to submit on behalf of
the copyright owner. For the purposes of this definition, "submitted"
means any form of electronic, verbal, or written communication sent
to the Licensor or its representatives, including but not limited to
communication on electronic mailing lists, source code control
systems, and issue tracking systems that are managed by, or on behalf
of, the Licensor for the purpose of discussing and improving the Work,
but excluding communication that is conspicuously marked or otherwise
designated in writing by the copyright owner as "Not a Contribution."

"Contributor" shall mean Licensor and any individual or Legal Entity
on behalf of whom a Contribution has been received by Licensor and
subsequently incorporated within the Work.

2. Grant of Copyright License. Subject to the terms and conditions of
this License, each Contributor hereby grants to You a perpetual,
worldwide, non-exclusive, no-charge, royalty-free, irrevocable
copyright license to use, reproduce, modify, display, perform,
sublicense, and distribute the Work and such Derivative Works in
Source or Object form.

... [Full Apache 2.0 license text continues]
```

### Open Logic
- **Repository**: https://github.com/open-logic/open-logic
- **License**: GNU Lesser General Public License v3.0 with FPGA exception
- **Usage**: Testing PyHDLio parser against modern FPGA standard library
- **Location**: `tests/projects/open-logic/`

The Open Logic library uses LGPL v3.0 with an FPGA exception that makes it commercial-friendly for hardware designs.

## PLY (Python Lex-Yacc)
- **Repository**: Included as submodule in `hdlio/submodules/ply/`
- **License**: BSD License
- **Usage**: Parser generation toolkit used by PyHDLio

## License Compliance

### Usage Scope
All third-party projects listed above are:
1. **Optional**: Not required for basic PyHDLio functionality
2. **Test-only**: Used only for testing and validation
3. **Not distributed**: Not included in PyHDLio releases
4. **Submodules**: Separately maintained with their own licenses

### Commercial Use
All included projects use licenses that are compatible with commercial use:
- **MIT License**: Permissive, commercial-friendly
- **Apache 2.0**: Permissive, commercial-friendly, patent protection
- **LGPL with FPGA exception**: Commercial-friendly for HDL/FPGA designs
- **BSD License**: Permissive, commercial-friendly

### Attribution Requirements
When using PyHDLio with these test projects:
1. **MIT/BSD**: Retain copyright notices in source code
2. **Apache 2.0**: Retain copyright notices and provide license text
3. **LGPL**: Comply with LGPL terms if modifying the libraries themselves

### No License Contamination
The use of these projects for testing does not affect PyHDLio's own licensing terms. PyHDLio remains under its original license regardless of which test projects are used.

For complete license texts, see the individual project directories:
- `tests/projects/en_cl_fix/LICENSE`
- `tests/projects/osvvm/LICENSE`
- `tests/projects/open-logic/LICENSE`
- `hdlio/submodules/ply/README.md` 