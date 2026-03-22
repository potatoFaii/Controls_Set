![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

# Controls_Set Tool — Rigger Guide

---

## Overview

**Controls_Set** is a rigging utility designed to help manage animation controller selection in production scenes.

The tool allows riggers to define a structured controller selection set that can later be used by animators for:

- Animation baking
- Animation layer cleanup
- Shot finalisation
- Export preparation

By centralising controller filtering and selection logic, the tool ensures that animators always operate on a complete and safe set of animation controls.

Control set data can be stored as **JSON presets**, allowing reuse across shots, rigs, or artists.

> ⚠️ This tool is intended for educational and personal workflow usage.

---

## Tool Architecture

The Controls_Set system is composed of:

- JSON-based filter preset
- Controller filtering logic
- UI builder for control set generation
- Outliner integration (visual feedback)
- Right-click workflow utilities

![ControlSet_UI](https://github.com/user-attachments/assets/203fcfd4-4d06-457a-9ef7-1096a0fb0e7f)

The tool may operate in two modes:

### Preset Mode
Uses stored JSON filter data to rebuild the control set.

### Scene Scan Mode
Scans the scene for potential controllers and applies exclusion filtering based on preset rules.

---

## Workflow Concept

### Main Window UI

When launching the Controls_Set UI:

- The tool attempts to load filter data from a JSON filepath
- If successfully loaded, the generated control set will be highlighted in **green in the Outliner**
- Riggers may choose between:
  - Building control set using preset include/exclude logic
  - Automatically scanning the scene and filtering controllers dynamically

After processing, the final `controls_Set` node is generated or updated.

---

### Right-Click Workflow

![FilterSetup_Function](https://github.com/user-attachments/assets/437f31af-d80e-4cf3-9ff4-f8a4d4b16dea)

Within the tool UI:

- Access **JSON → Filter Setup**
- This opens the **Filter Setup Builder UI**
- Used when:
  - No preset exists
  - New rig configuration is required
  - Filter logic must be adjusted

---

## Filter Setup Builder

![ControlSet_Compare_UI](https://github.com/user-attachments/assets/ff3bc603-a8e5-42c2-bf9c-f1a3b4422152)

The filter builder is divided into multiple functional rows.

### Row 1 — Scene Controller Scan

- Scans the scene for all `nurbsCurve` controller shapes
- Provides a base candidate list of animation controls

### Row 2 (Top) — Hierarchy Extraction

- Allows riggers to input a top null / group node
- Tool automatically collects all child controllers under the hierarchy

### Row 2 (Bottom) — Manual Filter Layer

- Allows inclusion or exclusion of selected nodes
- Used to refine automated scan results

### Row 3 — Final Output Builder

- Displays the final filtered controller list
- Allows exporting this list into JSON preset format
- Used to generate the final `controls_Set`

---

## Installation

1. Open **Autodesk Maya**
2. Drag and drop `ControlsSet_Install.mel` into the Maya viewport
3. A shelf button will be created automatically
4. Click the shelf button to initialize the tool environment

---

## Registering a New Rig

Recommended rigging workflow:

1. Launch **Filter Setup Builder**
2. Perform scene scan or hierarchy extraction
3. Refine controller list manually if needed
4. Export JSON preset
5. Generate `controls_Set`
6. Verify animator baking workflow

---

## Best Practices

- Avoid including deformation helper controllers (bendy / spline / setup controls)
- Ensure all animator-keyable controllers are included
- Validate behaviour in referenced rig scenarios
- Store JSON presets in version-controlled location
- Update presets when rig structure changes

---

## Known Limitations

- Namespace changes may require preset refresh
- Referenced rigs may need manual verification
- Non-standard controller shapes may not be auto-detected
- Dynamic rig rebuild may invalidate stored preset

---

## Credits

Workflow inspired by production rigging practices.

---

## Feedback & Contributions

This tool is under continuous iteration.

Riggers are encouraged to provide:

- Pipeline feedback
- Rig integration notes
- Edge case reports
- Performance observations

---

## License

Provided **as-is** for personal and educational use.
