# PyHDLio Licensing Summary

## Overview

PyHDLio is licensed under the GNU Lesser General Public License version 3 (LGPL v3), which provides a balance between open source requirements and practical usability for both open source and proprietary projects.

## License Files

The following license-related files have been added to the root directory:

### Core License Files

- **`LICENSE`** - The complete LGPL v3 license text
- **`COPYING`** - A copy of the LICENSE file (GNU project convention)
- **`COPYRIGHT`** - Copyright notice and project information
- **`LICENSE_HEADER.txt`** - Short license header for inclusion in source files

## LGPL v3 Key Features

### What LGPL v3 Allows

1. **Library Usage**: Applications can link to PyHDLio without being required to release their source code under LGPL
2. **Commercial Use**: PyHDLio can be used in commercial, proprietary applications
3. **Distribution**: You can distribute PyHDLio along with your applications
4. **Modification**: You can modify PyHDLio for your own use

### What LGPL v3 Requires

1. **Library Modifications**: If you modify PyHDLio itself, those modifications must be released under LGPL v3
2. **License Preservation**: You must include the LGPL license text when distributing PyHDLio
3. **Source Availability**: Modified versions of PyHDLio must have source code available
4. **Attribution**: You must preserve copyright notices and license information

### What LGPL v3 Does NOT Require

1. **Application Source**: Applications that use PyHDLio do not need to be open source
2. **Application License**: Your application can use any license you choose
3. **Linking Restrictions**: Static or dynamic linking to PyHDLio does not affect your application's license

## Practical Implications

### For Users of PyHDLio

- ✅ Use PyHDLio in commercial projects
- ✅ Use PyHDLio in proprietary software
- ✅ Distribute PyHDLio with your applications
- ✅ Keep your application's source code private
- ⚠️ Include PyHDLio's license when distributing
- ⚠️ Provide PyHDLio source code if requested

### For Contributors to PyHDLio

- ✅ Contribute improvements back to the project
- ✅ Fork and modify for your own use
- ⚠️ Modifications to PyHDLio must be LGPL v3
- ⚠️ Must make modified PyHDLio source available

## File Usage Guidelines

### For Source Files

Add the following header to Python source files:

```python
"""
This file is part of PyHDLio.

PyHDLio is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyHDLio is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with PyHDLio. If not, see <https://www.gnu.org/licenses/>.
"""
```

### For Distribution

When distributing PyHDLio:

1. Include the `LICENSE` or `COPYING` file
2. Include the `COPYRIGHT` file
3. Preserve all copyright notices in source files
4. Provide information on how to obtain the source code

## Compatibility

### Compatible Licenses

LGPL v3 is compatible with:
- GPL v3 (can be combined into GPL v3 projects)
- Apache 2.0 (one-way compatibility)
- MIT/BSD (can incorporate MIT/BSD code)
- Most permissive licenses

### Incompatible Licenses

LGPL v3 may have issues with:
- GPL v2 only (without "or later" clause)
- Some proprietary licenses with restrictive terms
- Licenses with patent retaliation clauses that conflict with LGPL v3

## Why LGPL v3 for PyHDLio?

### Benefits for the Project

1. **Encourages Contributions**: Improvements to PyHDLio itself must be shared back
2. **Prevents Proprietary Forks**: Core library remains open source
3. **Wide Adoption**: Allows use in both open source and commercial projects
4. **Patent Protection**: Includes patent grant and retaliation clauses

### Benefits for Users

1. **Commercial Friendly**: Can be used in proprietary applications
2. **No Viral Effect**: Your application code is not affected by LGPL
3. **Flexibility**: Multiple ways to comply with license requirements
4. **Legal Clarity**: Well-established license with clear terms

## Compliance Checklist

### For Application Developers

- [ ] Include PyHDLio license files in your distribution
- [ ] Preserve PyHDLio copyright notices
- [ ] Provide information on obtaining PyHDLio source
- [ ] If you modified PyHDLio, make those modifications available

### For PyHDLio Contributors

- [ ] Ensure contributions are compatible with LGPL v3
- [ ] Add appropriate license headers to new files
- [ ] Document any third-party code and its licenses
- [ ] Verify all dependencies are LGPL v3 compatible

## Additional Resources

- [GNU LGPL v3 Official Text](https://www.gnu.org/licenses/lgpl-3.0.html)
- [LGPL v3 FAQ](https://www.gnu.org/licenses/gpl-faq.html)
- [Free Software Foundation](https://www.fsf.org/)
- [SPDX License Identifier](https://spdx.org/licenses/LGPL-3.0-or-later.html): `LGPL-3.0-or-later`

## Contact

For licensing questions specific to PyHDLio, please:
1. Review this document and the official LGPL v3 text
2. Consult with your legal team for commercial use
3. Open an issue on the PyHDLio repository for clarification
4. Contact the project maintainers for specific licensing concerns

---

**Note**: This summary is for informational purposes only and does not constitute legal advice. For legal questions, please consult with a qualified attorney familiar with open source licensing. 