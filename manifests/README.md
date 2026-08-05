# 分片清单（Manifests）

每个manifest至少记录：分片ID、行数、域合同版本、生成器版本、内容哈希、分片状态、审计文件、修复血缘、总体规划位置、待完成审计和发布状态。

状态不得混用：generated_unreviewed、generated_unreviewed_repaired、approved_for_training和rejected是不同状态。