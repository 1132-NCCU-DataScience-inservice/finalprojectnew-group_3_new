# ================================================================
#  Air-Quality / Weather 資料清理 v3
#    ‒ 刪 8 欄 → 20 欄
#    ‒ AQI_pollutant 文字 → 數碼 (0–7, 0=NA)
#    ‒ 依指定「來源站 → 目標站」補欄位，並記錄補了幾筆
#    ‒ 彙整每檔／每欄 NA 比例
#    ‒ 全部以 UTF-8-BOM 寫回 （NA 保留為 "NA" 字樣）
# ================================================================

suppressPackageStartupMessages(library(dplyr))
options(stringsAsFactors = FALSE)

## ---------- 使用者可調 ----------
input_dir  <- "."   # .R 與 80 份原始檔放一起
output_dir <- "D:/Program/DataScience/Final_Project/1132_DS_Final_AirQuality/Clear_Feature"
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

## ---------- 共用設定 ----------
drop_cols <- c(
  "AQI_sitename", "AQI_county", "AQI_status",
  "AQI_windspeed", "AQI_winddirec",
  "AQI_longitude", "AQI_latitude", "AQI_siteid"
)

pollutant_map <- c(
  "細懸浮微粒" = 1L,
  "臭氧八小時" = 2L,
  "懸浮微粒"   = 3L,
  "二氧化氮"   = 4L,
  "二氧化硫"   = 5L,
  "臭氧"       = 6L,
  "一氧化碳"   = 7L
)

recode_pollutant <- function(x) {
  code <- pollutant_map[trimws(x)]
  code[is.na(code)] <- 0L
  as.integer(code)
}

write_utf8_bom <- function(df, path) {
  con <- file(path, open = "w", encoding = "UTF-8")
  writeChar("\ufeff", con, eos = NULL)   # BOM
  write.csv(df, con, row.names = FALSE)  # NA 仍寫 "NA"
  close(con)
}

## ---------- 補值「任務」清單 ----------
fill_tasks <- list(
  list(target = "三重_C0AI30_combined.csv",
       source = "菜寮_C0AD30_combined.csv",
       cols   = c("AQI_o3", "AQI_o3_8hr")),
  list(target = "大同_C0AI30_combined.csv",
       source = "中山_C0AH70_combined.csv",
       cols   = c("AQI_o3", "AQI_o3_8hr")),
  list(target = "左營_C0V810_combined.csv",
       source = "前金_C0V690_combined.csv",
       cols   = c("Weather_Tx", "Weather_RH"))
)

## ---------- 資料結構用來累積 ----------
na_summary     <- list()       # 每檔 NA 比率
processed_files <- character() # 避免重複處理
log_lines       <- character() # 補值記錄

## ---------- 一、先跑所有「補值對」 ----------
for (task in fill_tasks) {
  tgt_file <- file.path(input_dir, task$target)
  src_file <- file.path(input_dir, task$source)
  
  # 讀檔
  tgt <- read.csv(tgt_file, fileEncoding = "UTF-8-BOM",
                  na.strings = c("", "NA", "ND", "-"), check.names = FALSE)
  src <- read.csv(src_file, fileEncoding = "UTF-8-BOM",
                  na.strings = c("", "NA", "ND", "-"), check.names = FALSE)
  
  # 前處理
  tgt <- tgt[ , !(names(tgt) %in% drop_cols)]
  src <- src[ , !(names(src) %in% drop_cols)]
  tgt$AQI_pollutant <- recode_pollutant(tgt$AQI_pollutant)
  src$AQI_pollutant <- recode_pollutant(src$AQI_pollutant)
  
  # 補值
  for (col in task$cols) {
    need <- is.na(tgt[[col]]) & !is.na(src[[col]])
    n_filled <- sum(need)
    tgt[[col]][need] <- src[[col]][need]
    
    log_lines <- c(log_lines,
                   sprintf("%s ← %s  補 %s : %d 筆",
                           task$target, task$source, col, n_filled))
  }
  
  # 寫回
  write_utf8_bom(tgt, file.path(output_dir, basename(tgt_file)))
  write_utf8_bom(src, file.path(output_dir, basename(src_file)))
  
  # 收 NA 比率
  na_summary[[basename(tgt_file)]] <- colSums(is.na(tgt)) / 43584
  na_summary[[basename(src_file)]] <- colSums(is.na(src)) / 43584
  
  processed_files <- c(processed_files, basename(tgt_file), basename(src_file))
}

## ---------- 二、處理其餘檔案 ----------
all_files   <- list.files(input_dir, pattern = "_combined\\.csv$", full.names = TRUE)
other_files <- setdiff(all_files, file.path(input_dir, processed_files))

process_and_save <- function(f) {
  df <- read.csv(f, fileEncoding = "UTF-8-BOM",
                 na.strings = c("", "NA", "ND", "-"), check.names = FALSE)
  df <- df[ , !(names(df) %in% drop_cols)]
  df$AQI_pollutant <- recode_pollutant(df$AQI_pollutant)
  
  na_summary[[basename(f)]] <<- colSums(is.na(df)) / 43584
  write_utf8_bom(df, file.path(output_dir, basename(f)))
}
invisible(lapply(other_files, process_and_save))

## ---------- 三、輸出 NA 比率彙總 ----------
summary_df <- do.call(rbind, na_summary)
summary_df <- cbind(file = rownames(summary_df), summary_df)
rownames(summary_df) <- NULL
write_utf8_bom(summary_df,
               file.path(output_dir, "NA_ratio_summary.csv"))

## ---------- 四、輸出補值記錄 ----------
log_path <- file.path(output_dir, "fill_log.txt")
con_log  <- file(log_path, open = "w", encoding = "UTF-8")
writeChar("\ufeff", con_log, eos = NULL) # BOM
writeLines(c("各站補值紀錄（分母 43584 行）", log_lines), con_log)
close(con_log)

cat(paste(log_lines, collapse = "\n"), "\n")
cat("\n✅ 全部完成！已輸出至：\n  ", output_dir, "\n")
