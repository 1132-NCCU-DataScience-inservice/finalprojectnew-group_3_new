library(zoo)
library(readr)

# ----------- 純R KNN補值 -------------
impute_knn <- function(x, k = 5) {
  if (all(!is.na(x))) return(x)
  na_idx <- which(is.na(x))
  avail  <- which(!is.na(x))
  out <- x
  for (i in na_idx) {
    d  <- abs(avail - i)
    if (length(avail) == 0) next  # 全部NA就跳過
    nn <- avail[order(d)[1:min(k, length(avail))]]
    out[i] <- mean(x[nn], na.rm = TRUE)
  }
  return(out)
}

impute_linear <- function(x, maxgap = 6) {
  na.approx(x, maxgap = maxgap, rule = 2)
}

impute_season <- function(x, hour_vec, wday_vec) {
  med_mat <- with(
    data.frame(h = hour_vec, w = wday_vec, v = x),
    tapply(v, list(h, w), median, na.rm = TRUE)
  )
  res <- x
  na_idx <- which(is.na(x))
  for (i in na_idx) {
    h <- as.character(hour_vec[i])
    w <- as.character(wday_vec[i])
    if (!is.na(med_mat[h, w])) {
      res[i] <- med_mat[h, w]
    }
  }
  return(res)
}

fill_na_by_length <- function(x, hour_vec, wday_vec, col_name = "") {
  n <- length(x)
  i <- 1
  out <- x
  while (i <= n) {
    if (is.na(x[i])) {
      j <- i
      while (j <= n && is.na(x[j])) j <- j + 1
      seg_idx <- if (j - 1 > n) i:n else i:(j - 1)
      seg_len <- length(seg_idx)
      # 印出段落與等級
      if (seg_len < 6) {
        cat(sprintf("[Level 1] %s rows %d-%d：線性插值\n", col_name, min(seg_idx), max(seg_idx)))
        tmp <- x
        tmp[seg_idx] <- NA
        out[seg_idx] <- impute_linear(tmp, maxgap = 6)[seg_idx]
      } else if (seg_len >= 6 & seg_len <= 24) {
        cat(sprintf("[Level 2] %s rows %d-%d：KNN補值\n", col_name, min(seg_idx), max(seg_idx)))
        tmp <- x
        tmp[seg_idx] <- NA
        out[seg_idx] <- impute_knn(tmp)[seg_idx]
      } else {
        cat(sprintf("[Level 3] %s rows %d-%d：同時期均值補值\n", col_name, min(seg_idx), max(seg_idx)))
        out[seg_idx] <- impute_season(x, hour_vec, wday_vec)[seg_idx]
      }
      i <- j
    } else {
      i <- i + 1
    }
  }
  return(out)
}

# ----------- 欄位規格修正與小數處理 -------------
format_features <- function(df) {
  spec_list <- list(
    AQI_aqi       = c(0, 100000),
    AQI_so2       = c(0, 100000),
    AQI_co        = c(0, 100000),
    AQI_o3        = c(0, 100000),
    AQI_o3_8hr    = c(0, 100000),
    AQI_pm10      = c(0, 100000),
    AQI_pm2.5     = c(0, 100000),
    AQI_no2       = c(0, 100000),
    AQI_nox       = c(0, 100000),
    AQI_no        = c(0, 100000),
    AQI_co_8hr    = c(0, 100000),
    AQI_pm2.5_avg = c(0, 100000),
    AQI_pm10_avg  = c(0, 100000),
    AQI_so2_avg   = c(0, 100000),
    Weather_Tx    = c(-20, 50),
    Weather_RH    = c(0, 100),
    Weather_WS    = c(0, 1000),
    Weather_WD    = c(0, 360)
  )
  # 修正範圍
  for (col in names(spec_list)) {
    if (col %in% names(df)) {
      rng <- spec_list[[col]]
      df[[col]] <- pmax(pmin(df[[col]], rng[2]), rng[1])
    }
  }
  # 修正小數位
  cols_1f <- c("AQI_so2", "AQI_co_8hr", "Weather_Tx", "Weather_WS")
  cols_2f <- c("AQI_co")
  for (col in names(df)) {
    if (col %in% cols_1f) df[[col]] <- round(df[[col]], 1)
    else if (col %in% cols_2f) df[[col]] <- round(df[[col]], 2)
    else if (col %in% names(spec_list)) df[[col]] <- round(df[[col]], 0)
  }
  return(df)
}

# ----------- UTF-8 BOM寫入 -------------
write_utf8_bom <- function(df, path) {
  temp <- tempfile()
  write.csv(df, temp, row.names = FALSE, fileEncoding = "UTF-8", quote = TRUE)
  dat <- readLines(temp, encoding = "UTF-8")
  con <- file(path, open = "wb") # 用二進位模式打開
  writeBin(charToRaw("\xEF\xBB\xBF"), con) # BOM
  writeLines(dat, con, useBytes = TRUE)
  close(con)
  unlink(temp)
}

# ============ 主批次處理流程 ============

input_folder <- "." # 程式與資料同目錄
output_folder <- "D:/Program/DataScience/Final_Project/1132_DS_Final_AirQuality/Final_Dataset"

if (!dir.exists(output_folder)) dir.create(output_folder, recursive = TRUE)

file_list <- list.files(input_folder, pattern = "\\.csv$", full.names = TRUE)

for (file_path in file_list) {
  df <- readr::read_csv(file_path, locale = locale(encoding = "UTF-8"), show_col_types = FALSE)
  message("Processing: ", basename(file_path))
  
  # 補值處理
  if ("date" %in% colnames(df)) {
    df$date <- as.POSIXct(df$date, tz = "UTC")
    hour_vec <- as.integer(format(df$date, "%H"))
    wday_vec <- as.integer(format(df$date, "%u"))
  } else {
    hour_vec <- rep(NA, nrow(df))
    wday_vec <- rep(NA, nrow(df))
  }
  for (col in colnames(df)) {
    if (col == "date" | col == "AQI_pollutant") next
    if (!is.numeric(df[[col]])) next
    if (all(!is.na(df[[col]]))) next
    df[[col]] <- fill_na_by_length(df[[col]], hour_vec, wday_vec, col_name = col)
  }
  # 範圍與小數位處理
  df <- format_features(df)
  # 時間欄位轉ISO8601
  if ("date" %in% colnames(df)) {
    df$date <- format(as.POSIXct(df$date, tz = "UTC"), "%Y-%m-%dT%H:%M:%SZ")
  }
  # 寫檔（UTF-8 BOM）
  out_path <- file.path(output_folder, basename(file_path))
  write_utf8_bom(df, out_path)
  message("Finish: ", out_path)
}

message("全部補值&寫檔完成!！")
