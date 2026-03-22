![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

# Controls_Set for Autodesk Maya

---

## Overview

**Controls_Set** is a utility tool designed to help animators perform final animation cleanup more efficiently.

In many production rigs, certain controllers are hidden, nested inside sets, or toggled via attributes.  
This can make it difficult for animators to manually select all required controls when performing tasks such as:

- Baking animation
- Cleaning animation layers
- Final polishing before publish

Missing even a few controllers during selection may lead to incomplete baking or unexpected rig behavior.

To solve this workflow issue, **Controls_Set** allows riggers to provide animators with a reliable way to select all relevant animation controls through set membership — without needing to hunt for controllers in the viewport or Outliner.

> ⚠️ This tool is intended for personal workflow and educational usage.

---

## Features

- Select all keyable animation controllers from a predefined control set
- Prevent accidental selection of technical or deformation controls (e.g. bendy rigs, IK spline helpers, setup nodes)
- Improve reliability of animation baking and cleanup workflows
- Reduce risk of missing hidden or attribute-toggled controllers

---

## Workflow Concept

### Accessing the Control Set

1. Open the **Outliner**
2. Locate the rig's `controls_Set`
3. **Right-click the set → Select Set Members**

Once selected, animators can safely:

- Bake animation
- Clean animation layers
- Perform final animation polish
- Prepare shots for publishing or handoff

This ensures that all necessary animation controls are included.

---

## Usage

1. Locate and select the provided control set
2. Perform animation baking or cleanup operations as required
3. Continue normal animation workflow with confidence that no critical controllers were missed

---

## Credits

Original workflow concept developed within production rigging practices.

---

## Feedback & Contributions

This is an evolving workflow tool.

Production feedback, improvements, and suggestions are highly appreciated.  
Feel free to open an issue or share ideas for further enhancement.

---

## License

Provided **as-is** for personal and educational use.
