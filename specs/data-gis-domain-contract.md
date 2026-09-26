# Data/GIS Domain Contract

## Purpose

The Data/GIS foundation models immutable datasets, spatial references, data layers, analysis requirements, and compatible planning tools.

## Contracts

- DataKind identifies tabular, raster, vector, and time-series data.
- LayerRole distinguishes source, derived, and output layers.
- SpatialReference captures reference-system identity and classification.
- DataLayer identifies a typed layer and optional spatial reference.
- DataProject defines the supported data scope and validates layer membership.
- DataAnalysisRequirement declares required data type, capabilities, and optional spatial-reference class.
- DataTool declares supported data kinds, capabilities, spatial-reference classes, and enabled state.
- DataGISPlanner deterministically normalizes inputs and produces bounded compatibility plans.

## Boundary

No GIS engine execution, rendering, geoprocessing execution, filesystem mutation, network access, subprocess execution, credential access, or host mutation.
