# 1. 載入套件
library(dplyr)
library(readr)
library(stringr)

# 2. 讀取對應表並處理多個工廠欄位＋Seq
mapping_file <- "D:/Program/DataScience/Final_Project/1132_DS_Final_AirQuality/Original_Dataset/AQStation_Corresponds_WeatherStation_2.csv"
mapping <- read.csv(
  mapping_file,
  fileEncoding  = "CP950",
  stringsAsFactors = FALSE
) %>%
  mutate(
    Factory_city     = as.numeric(gsub(",", "", 縣市內工廠總數)),
    Factory_district = as.numeric(gsub(",", "", 行政區內工廠數)),
    label            = Seq
  ) %>%
  select(
    station = 空品站名,
    Factory_city,
    Factory_district,
    label
  )

# 3. 設定要處理的資料夾路徑並列出所有 *_combined.csv
data_dir <- "D:/Program/DataScience/Final_Project/1132_DS_Final_AirQuality/Final_Dataset"
files <- list.files(
  path       = data_dir,
  pattern    = "_combined\\.csv$",
  full.names = TRUE
)

# 4. 自訂函式：先寫 BOM，再以 UTF-8 文字連線 append CSV
write_utf8_bom <- function(df, path) {
  # (a) 二進位連線寫入 UTF-8 BOM
  bin_con <- file(path, open = "wb")
  writeBin(as.raw(c(0xEF, 0xBB, 0xBF)), bin_con)
  close(bin_con)
  # (b) 文字連線以 UTF-8 編碼 append CSV 內容
  txt_con <- file(path, open = "a", encoding = "UTF-8")
  write.csv(df, txt_con, row.names = FALSE)
  close(txt_con)
}

# 5. 逐檔讀入、加上所有四個 mapping 欄位，並記錄無對應 mapping 的檔案
missing <- character()
df_list <- list()

for (f in files) {
  fname <- basename(f)
  station_name <- str_split(fname, "_", simplify = TRUE)[1, 1]
  
  if (! station_name %in% mapping$station) {
    missing <- c(missing, fname)
    next
  }
  
  # 取該站對應的所有欄位
  mr <- mapping %>% filter(station == station_name) %>% slice(1)
  fac_city   <- mr$Factory_city
  fac_dist   <- mr$Factory_district
  lab         <- mr$label
  
  # 讀檔：保留 date 欄的 T…Z 原始字串
  df <- read_csv(
    f,
    locale    = locale(encoding = "UTF-8"),
    col_types = cols(date = col_character())
  )
  
  # 新增四個欄位
  df <- df %>% mutate(
    Factory_city      = fac_city,
    Factory_district  = fac_dist,
    label             = lab
  )
  
  df_list[[length(df_list) + 1]] <- df
}

# 6. 合併所有資料並寫出最終 CSV
combine_traindata <- bind_rows(df_list)
out_path <- file.path(data_dir, "Combine_AllData.csv")
write_utf8_bom(combine_traindata, out_path)

# 7. 列印結果
cat("===== 無對應 mapping，已跳過下列檔案 =====\n")
if (length(missing) > 0) cat(paste(missing, collapse = "\n"), "\n")
cat(sprintf("總共 %d 個檔案沒有找到 mapping\n", length(missing)))
cat("最終檔案已寫出到：", out_path, "\n")
