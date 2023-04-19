# Sessile Organism Range

Python-based ArcGIS toolbox for assessing the ranges of species (i.e., NOT the home ranges of individuals).

## Getting Started

These instructions will enable you to run the Plant Range Toolbox in ArcGIS Pro or Desktop.

### Prerequisites
Required: ArcGIS Pro 2.0 or higher AND/OR ArcGIS Desktop 10.4.1
Recommended: 64-bit Background Processing if using ArcGIS Desktop

### Installing

Download this repository and unzip it to a folder on a drive accessible to your computer. Local drives may perform better than network drives.

Open ArcGIS Pro or ArcMap:
* In ArcGIS Pro, open the catalog tab, right click on the toolbox folder, select add toolbox, and navigate to the location of the downloaded/unzipped toolbox.
* In ArcMap, open the toolbox tab, right click, select add toolbox, and navigate to the location of the downloaded/unzipped toolbox.

*The toolbox and the script folder must remain in the same parent folder or the location of the script will have to be modified in the toolbox.*

## Usage

### Concave Hull from Occurrence Points
* "Input Points" should be a shapefile of species occurrence points (presences-only). No attribute values are used in the tool calculations.
* "Clip Dataset" is optional. If selected, the concave hull calculated from the input points will be clipped to the polygon to produce a final output. This is useful when producing continental or trans-continental ranges that should not include oceans or marine ranges that should not include terrestrial regions.
* "Workspace" folder is a folder in which temporary products will be stored until the tool finishes. "Workspace" should be empty.
* "Output Concave Hull" is the shapefile that will store the final polygon(s).
* "Minimum Search Distance" is the minimum distance between points that will be used to calculate the aggregation distance. A minimum search distance of 1,000 m is appropriate for most uses.
* "Buffer Distance" is the distance beyond the minimum point boundary that will be included in the final range. The buffer distance should reflect expert opinion, uncertainty in the species occurrence point dataset, and the scale of the analysis. 50 km is appropriate for ranges at trans-continental scales.
* "Modification Value" is a scale-dependent multiplicative factor that adjusts the aggregation distance. The modification value is dependent on the scale of the analysis and the spatial consistency of input points. A modification value of 8 is appropriate for many trans-continental analyses and is a good starting point that can be adjusted up or down.

## Credits

### Built With
* ArcGIS Desktop 10.4.1
* ArcGIS Pro 2.0
* Notepad ++

### Authors

* **Timm Nawrocki** - *Alaska Center for Conservation Science, University of Alaska Anchorage*

### Usage Requirements

If you use this tool, elements of this tool, or a derivative product, please cite the following:

Carlson, M.L., E.J. Trammell, T.W. Nawrocki, and E. Noongwook. 2018. Additions to the vascular flora of St. Lawrence Island, Alaska: new records, rare species, and phytogeographic patterns. Rhodora. 120:1-41.

### License

This project is provided under the GNU General Public License v3.0. It is free to use and modify in part or in whole.
