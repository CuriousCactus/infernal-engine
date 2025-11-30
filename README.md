# Infernal Engine

A tool for converting Baldur's Gate 3 mocap animations into timeline animations.
This means you can have more natural looking gesturing in your new timelines without having to record your own mocap.

## Features

* Finds the mocap GR2 file for a particular line and copies to your Public folder with a sensible folder structure and file name.
* Creates a metadata file so that the animation is ready to use in timelines.

You just need to search for a line you like the mocap for in [Norbyte's search tool](https://bg3.norbyte.dev/search?iid=Dialog.13a14528-0975-89d9-0053-a79b6ecd748f), then find the line 'handle'. For example, here you want `he42b911eg0df6g49dfgbe0dgc764805b8593` (N.B. without the `;4` at the end):

```
<TagText>
	<!-- Free. I never thought I would be, believed I could be, <b>hoped</b> I might be. -->
	<TagText>he42b911eg0df6g49dfgbe0dgc764805b8593;4</TagText>
	<LineId>d5cc305e-f1f4-4d40-a2a8-71b9c99f352d</LineId>
	<stub>True</stub>
</TagText>
```

You will also need:

* The dialog file name without the extension, in this case `LOW_HouseOfHope_Hope`.
* Your game data path.
* Your unpacked data path (generated with the [Modder's Multitool](https://github.com/ShinyHobo/BG3-Modders-Multitool)).
* Your mod name, including the guid on the end.
* The path to `Divine.exe` from [LSLib](https://github.com/Norbyte/lslib).

## Building

To work on this app, first create a virtual environment to work in:

```
python -m venv .venv 
```

Activate it:

```
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```
pip install -e .
```

Run the build tool:

```
pyinstaller .\src\infernal_engine\main.py -F -n InfernalEngine.exe --add-data=template_files:template_files
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
