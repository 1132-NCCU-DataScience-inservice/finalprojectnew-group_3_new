#!/usr/bin/env Rscript
# ================================================================================
# AQI 模型高速評估系統 - 專為大量模型快速分析設計
# ================================================================================

cat("⚡ AQI 模型高速評估系統啟動...\n")
cat("📅 執行時間:", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n")

# ================================================================================
# 1. 高速模式配置
# ================================================================================

configure_fast_mode <- function() {
  cat("\n⚙️ 設定高速分析模式...\n")
  
  # 核心加速設定
  Sys.setenv(SHAP_MODE = "fast")           # 快速 SHAP 模式
  Sys.setenv(AQI_FULL_EVAL = "true")      # 全量評估
  
  # 並行處理設定 (Windows 不支援)
  if(.Platform$OS.type != "windows") {
    Sys.setenv(USE_PARALLEL = "true")     # 啟用並行處理
    Sys.setenv(PARALLEL_CORES = "16")      # 使用 16 核心
    cat("   🚀 並行處理: 啟用 (16 核心)\n")
  } else {
    Sys.setenv(USE_PARALLEL = "false")    # Windows 停用並行
    cat("   ⚠️ 並行處理: 停用 (Windows 不支援)\n")
  }
  
  # 記憶體優化設定
  Sys.setenv(MAX_MEMORY_GB = "55")         # 最大記憶體使用 55GB
  Sys.setenv(CLEANUP_INTERVAL = "5")      # 每 5 個模型清理記憶體
  
  cat("✅ 高速模式配置完成:\n")
  cat("   🔥 SHAP 模式: 快速 (2樣本, 20特徵, 10迭代)\n")
  cat("   💾 記憶體控制: 55GB 限制\n")
  speed_boost <- if(.Platform$OS.type != "windows") "5-10x" else "3-5x"
  cat("   ⚡ 預估速度提升:", speed_boost, "\n")
}

# ================================================================================
# 2. 效能監控
# ================================================================================

performance_monitor <- function() {
  list(
    start_time = Sys.time(),
    models_processed = 0,
    errors_count = 0,
    
    update = function(models_count = 1, has_error = FALSE) {
      .self <- environment()
      .self$models_processed <- .self$models_processed + models_count
      if(has_error) .self$errors_count <- .self$errors_count + 1
      
      elapsed <- as.numeric(difftime(Sys.time(), .self$start_time, units = "mins"))
      speed <- .self$models_processed / max(elapsed, 0.1)
      
      cat(sprintf("📊 進度: %d 模型 | %.1f 分鐘 | %.1f 模型/分鐘 | %d 錯誤\n",
                 .self$models_processed, elapsed, speed, .self$errors_count))
    },
    
    summary = function() {
      .self <- environment()
      total_time <- as.numeric(difftime(Sys.time(), .self$start_time, units = "mins"))
      avg_speed <- .self$models_processed / max(total_time, 0.1)
      
      cat("\n📈 效能摘要:\n")
      cat("   總處理時間:", round(total_time, 2), "分鐘\n")
      cat("   處理模型數:", .self$models_processed, "\n")
      cat("   平均速度:", round(avg_speed, 1), "模型/分鐘\n")
      cat("   錯誤率:", round(.self$errors_count / max(.self$models_processed, 1) * 100, 1), "%\n")
    }
  )
}

# ================================================================================
# 3. 智能批次處理
# ================================================================================

smart_batch_analysis <- function(registry, max_models = NULL) {
  monitor <- performance_monitor()
  
  cat("\n🎯 開始智能批次分析...\n")
  
  # 過濾有效模型
  valid_models <- registry[!is.na(test_rmse)]
  if(!is.null(max_models)) {
    valid_models <- head(valid_models[order(test_rmse)], max_models)
  }
  
  cat("📋 將分析", nrow(valid_models), "個有效模型\n")
  
  # 按模型類型和大小分組
  lgbm_models <- valid_models[model_type == "lgbm"]
  lstm_models <- valid_models[model_type == "lstm"]
  
  # 按檔案大小排序 (小檔案優先，避免記憶體問題)
  lgbm_models <- lgbm_models[order(model_size_mb)]
  lstm_models <- lstm_models[order(model_size_mb)]
  
  results <- list()
  
  # 分析 LGBM 模型
  if(nrow(lgbm_models) > 0) {
    cat("\n🌳 分析", nrow(lgbm_models), "個 LGBM 模型...\n")
    lgbm_results <- run_model_analysis(lgbm_models, n_top_models = nrow(lgbm_models))
    results$lgbm <- lgbm_results
    monitor$update(nrow(lgbm_models))
  }
  
  # 清理記憶體
  cleanup_memory(verbose = TRUE)
  
  # 分析 LSTM 模型
  if(nrow(lstm_models) > 0) {
    cat("\n🧠 分析", nrow(lstm_models), "個 LSTM 模型...\n")
    lstm_results <- run_model_analysis(lstm_models, n_top_models = nrow(lstm_models))
    results$lstm <- lstm_results
    monitor$update(nrow(lstm_models))
  }
  
  monitor$summary()
  return(results)
}

# ================================================================================
# 4. 快速報告生成
# ================================================================================

generate_fast_report <- function(results, registry) {
  cat("\n📊 生成快速分析報告...\n")
  
  # 基本統計
  total_models <- nrow(registry)
  valid_models <- sum(!is.na(registry$test_rmse))
  best_rmse <- min(registry$test_rmse, na.rm = TRUE)
  
  # 按類型統計
  lgbm_count <- sum(registry$model_type == "lgbm")
  lstm_count <- sum(registry$model_type == "lstm")
  
  # 生成簡要報告
  report_content <- c(
    "# AQI 模型高速評估報告",
    "",
    paste("**執行時間:**", Sys.time()),
    paste("**分析模式:** 高速並行模式"),
    "",
    "## 模型統計",
    paste("- 總模型數:", total_models),
    paste("- 有效模型數:", valid_models),
    paste("- LGBM 模型:", lgbm_count),
    paste("- LSTM 模型:", lstm_count),
    paste("- 最佳 RMSE:", round(best_rmse, 4)),
    "",
    "## 最佳模型 Top 10",
    ""
  )
  
  # 添加 Top 10 模型
  top_models <- registry[!is.na(test_rmse)][order(test_rmse)][1:min(10, valid_models)]
  for(i in 1:nrow(top_models)) {
    model <- top_models[i]
    report_content <- c(report_content,
      paste(i, ".", model$model_id, "- RMSE:", round(model$test_rmse, 4), 
            "(", model$model_type, ",", model$model_size_mb, "MB)")
    )
  }
  
  # 保存報告
  report_file <- "analysis_outputs/fast_evaluation_report.md"
  dir.create(dirname(report_file), recursive = TRUE, showWarnings = FALSE)
  writeLines(report_content, report_file)
  
  cat("✅ 快速報告已保存:", report_file, "\n")
}

# ================================================================================
# 5. 主程式
# ================================================================================

main_fast <- function(max_models = 50) {
  cat("🚀 AQI 高速評估主程式啟動\n")
  cat(paste(rep("=", 50), collapse=""), "\n")
  
  start_time <- Sys.time()
  
  tryCatch({
    # 1. 配置高速模式
    configure_fast_mode()
    
    # 2. 載入模組
    cat("\n📦 載入分析模組...\n")
    source("model_src/explainer.R")
    
    # 3. 生成註冊表
    cat("\n📋 生成模型註冊表...\n")
    registry <- generate_model_registry()
    
    if(nrow(registry) == 0) {
      stop("❌ 沒有找到任何模型檔案")
    }
    
    cat("✅ 找到", nrow(registry), "個模型\n")
    
    # 4. 智能批次分析
    results <- smart_batch_analysis(registry, max_models)
    
    # 5. 生成快速報告
    generate_fast_report(results, registry)
    
    # 6. 生成全量評估摘要
    full_summary <- generate_full_evaluation_summary(registry, "analysis_outputs")
    
    total_time <- as.numeric(difftime(Sys.time(), start_time, units = "mins"))
    
    cat("\n🎉 高速評估完成！\n")
    cat("⏱️ 總執行時間:", round(total_time, 2), "分鐘\n")
    cat("🚀 速度提升: 約", round(max_models / max(total_time, 0.1), 1), "模型/分鐘\n")
    
    # 清理資源
    cleanup_memory(verbose = TRUE)
    
    return(list(
      results = results,
      registry = registry,
      execution_time = total_time
    ))
    
  }, error = function(e) {
    cat("\n❌ 高速評估失敗:\n")
    cat("錯誤訊息:", e$message, "\n")
    return(NULL)
  })
}

# ================================================================================
# 執行選項
# ================================================================================

# 從命令列參數獲取最大模型數
args <- commandArgs(trailingOnly = TRUE)
max_models <- if(length(args) > 0) as.numeric(args[1]) else 30

cat("\n💡 使用方法:\n")
cat("  Rscript demo_fast_evaluation.R [最大模型數]\n")
cat("  範例: Rscript demo_fast_evaluation.R 50\n")
cat("\n")

if(!interactive()) {
  # 腳本模式執行
  cat("🎯 分析前", max_models, "個最佳模型\n")
  results <- main_fast(max_models)
} else {
  # 互動模式
  cat("💡 互動模式已載入，執行 main_fast(50) 開始快速分析\n")
} 