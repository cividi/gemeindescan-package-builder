# Gemeindescan Data Package builder

A template to generate valid [Gemeindescan](https://bitbucket.org/cividi/gemeindescan-webui) datapackages.

## Quick Start

- add your styled geojsons (according to the simplestyles spec) in `project/data/`
- add your snapshot metadata in the `project.yml`
- install [YAML support](https://yaml.readthedocs.io/en/latest/install.html) using `python package-builder.py`
- run `python package-builder.py` after changing `project` to your folder/yml file name. For more details refer to the spec description below.

## Walkthrough

Adapt the `template.yml` to capture your default settings for a single snapshot and an entry in the legend.

Then copy the `sample-project`, add your styled geojsons (according to the simplestyles spec) in `project/data/` and add your snapshot metadata in the `project.yml`. Then just run `python package-builder.py` after changing `project` to your folder/yml file name. For more destails refer to the spec description below.

```sh
export PROJECT=project
mkdir $PROJECT && mkdir $PROJECT/data && mkdir $PROJECT/snapshots
cp sample-project/sample-project.yml $PROJECT/$PROJECT.yml

# Edit new .yml, add data

pip install -r requirements.txt
python package-builder.py -p $PROJECT
```

## CLI options

Run

```sh
python package-builder.py --help
```

to see available options.

## Makefile

```sh

export PROJECT="project"
make init

# Edit project/project.yml, add data, ...

make

``` 

## project.yml Spec

### legends

This is where the Legends entries live. The top level item has to match the resource name given in the snapshot resources, which is also what the geojson is called.

```yml
legends:
    "sample-hr-adressen":
        "Gebäude mit Handelsregistereintrag":
            fillColor: "#93bddf"
            fillOpacity: 1
            stroke: "#000000"
            strokeWidth: 2
            strokeOpacity: 1
            primary: true
```

Each entry becomes one legend item, with `Gebäude mit Handelsregistereintrag` becoming the label.
In the Styling as little or as many of the possible entries (fillColor, fillOpacity, stroke, strokeWidth, strokeOpacity and primary) can be used. If a value is not present its counterpart from the template.yml is used.

Entries with the `primary` flag are shown all on all map versions, whereas non primary entries are hidden by default and can be expanded by the user.

### snapshots

Each entry here becomes a .json file inside the `snapshots/` folder after running the builder.

```yml
snapshots:
    - sample-hr-adressen:
        title: "Gebäude mit Handelsregistereinträgen"
        description: "Gebäude mit Adressen, die mindestens einen Handelsregistereintrag aufweisen."
        keywords:
            - sample
        gemeindescan_meta:
            topic: "Struktur"
        bounds:
            - "geo:47.073023,8.359509"
            - "geo:47.076802,8.365662"
        resources:
            - "sample-hr-adressen":
                mediatype: "application/geo+json"
        sources:
            -
                url: "https://www.housing-stat.ch"
                title: "Handelsregistereinträge: Handelsregister Kanton Luzern"
            -
                url: "https://rawi.lu.ch/themen/amtliche_vermessung"
                title: "Bodenbedeckung, Amtliche Vermessung, Kanton Luzern"
        attribution: ""
        maintainers:
            -
                name: "Luis Gisler"
                web: "https://github.com/cividitech/"
```

`Bounds` are the view bounds used to position the snapshot on screen upon loading. `Resources` are used to load geojsons from the `data/` directory. Note that the resource name has to match the geojson file name as well as the corresponding legend name to work properly. Whereas the snapshot name (in this case also `sample-hr-adressen`) is used for the resulting .json file in `snapshots/` and is unrelated to the geojson and legends.

Addionally, `sources`, an attribution and additional maintainers can be specified and will be added to the ones in `template.yml`.
