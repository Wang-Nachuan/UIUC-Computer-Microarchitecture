# Frequently Used Commands

Configuration file locations
```bash
# Design config file (top): generators/chipyard/src/main/scala/config/BoomConfigs.scala
# Design config file (detail): generators/boom/src/main/scala/common/config-mixins.scala
# Design source file: generators/boom/src/main/scala/...
# FPGA config file: fpga/src/main/scala/vcu118/Configs.scala
```

BOOM Project Hierarchy (~=chipyard/generator/boom/src/main/scala)
```
BoomTile (~/common/tile.scala)
--> BoomTileModuleImp (~/common/tile.scala)
    --> LSU (~/lsu/lsu.scala)
--> BoomNonBlockingDCache (~/lsu/dcache.scala)
    --> BoomNonBlockingDCacheModule (~/lsu/dcache.scala)
        --> BoomMSHRFile (~/lsu/mshrs.scala)
            --> LAPrefetcher (~/lsu/prefetcher.scala)
```

Compile the design

```bash
# From: sims/verilator/
# Result: sims/verilator/

make CONFIG=<design_config_name>
```

Run benchmarks

```bash
# From: sims/verilator/
# Result: sims/verilator/output/<*design_config_name>/

make CONFIG=<design_config_name> run-bmark-tests
```

Shortcut
```bash
make CONFIG= && make CONFIG= run-bmark-tests
```

Generate bitstream

```bash
# From: fpga
# Result: fpga/generated-src/<*fpga_config_name>/obj/*.bit

make SUB_PROJECT=vcu118 CONFIG=<fpga_config_name> bitstream
```