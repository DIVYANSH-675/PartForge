# PartForge

A command-array quality gate for Img2CAD exports.

An extension maintained by Divyansh Gupta, based on [https://github.com/qq456cvb/Img2CAD](https://github.com/qq456cvb/Img2CAD) at `afe48afa3f66e793ac9b64d3df4aab8c3ef7f7e3`. Upstream source, licenses, citations and commit history are preserved. See [upstream documentation](UPSTREAM_README.md).

## Added functionality

Checks 17-column command arrays, nonfinite values, unknown commands, missing loops/extrusions and commands after EOS. Supports the native HDF5 `vec` dataset when h5py is installed. Reports each input independently and exits nonzero if any input fails.

## Quick start

The new utility uses Python 3.10+ and the standard library. The examples are synthetic. GPU packages are not required for the new utility or its tests.

```bash
python3 partforge.py examples/cad.json --output report.json
python3 -m unittest discover -s tests -v
```

## Scope and limitations

This validates command structure, not geometry, dimensional accuracy, manufacturability or printability. Image inference still requires the upstream model, data and dependencies. No accuracy improvement is claimed.

## Licensing

The new `partforge.py`, its tests, synthetic examples, CI workflow and this README are MIT licensed in ADDITIONS_LICENSE. Upstream files retain their existing notices and terms; the new license does not relicense them.
