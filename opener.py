import pystac
import fsspec
import xarray as xr

assert int(pystac.__version__[0]) == 1, "pystac version must be >= 1.0.0"

ENDPOINT = "https://raw.githubusercontent.com/cisaacstern/pangeo-forge-catalog/reorg/stac"


def open_zarr_asset(path, asset):
    """
    Parameters
    ----------
    path: str
        Path to a valid STAC Item implementing `xarray-assets`
        extension and including zarr store Asset.
    asset: str
        Name of zarr store Asset.
    
    Returns
    -------
    xarray.Dataset
    """
    path = f"{ENDPOINT}/{path}"
    item = pystac.read_file(path)
    asset = item.assets[asset]
    store = fsspec.get_mapper(asset.href, **asset.extra_fields["xarray:storage_options"])
    return xr.open_zarr(store, **asset.extra_fields["xarray:open_kwargs"])
