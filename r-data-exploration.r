library(tidyverse)
library(lubridate)
library(repr)
library(ggthemes)
library(forecast)

monthly_core_metrics <- read_csv('./downloads/RDC_Inventory_Core_Metrics_Zip_History.csv',col_types = cols(postal_code = col_character(), zip_name 
                                                                                                          = col_character()))

zip_filter <- read_csv('./zipcodes.csv', col_types = cols(zipcode = col_factor()))

filtered_zips_df <- monthly_core_metrics %>%
    mutate(date = ym(month_date_yyyymm)) %>%
    select(-month_date_yyyymm) %>%
    head(-2) %>%
    mutate(postal_code = ifelse(str_length(postal_code) == 4, paste0('0',postal_code), postal_code)) %>%
    mutate(postal_code = as_factor(postal_code)) %>%
    semi_join(x = ., y = zip_filter, by = c("postal_code" = "zipcode"))

monthly_totals <- filtered_zips_df %>%
    select(date, active_listing_count) %>%
    group_by(date) %>%
    summarize(active_listing_count = sum(active_listing_count)) %>%
    arrange(date)
head(monthly_totals,10)

options(repr.plot.width=18, repr.plot.height=10)
monthly_listings_plot <- ggplot(monthly_totals, aes(x=date, y=active_listing_count)) +
    geom_line() + 
    theme_gdocs() +
    labs() + 
    ylim(0, 700) +
    scale_x_date(date_minor_breaks = "1 month", date_labels = "%b %Y")

monthly_listings_plot

monthly_listing_ts <- ts(monthly_totals$active_listing_count, frequency=12, start = c(2016, 07), end = c(2020, 12))
hw <- HoltWinters(monthly_listing_ts)
hw_fc <- forecast(hw, h = 12, findfrequency = TRUE)
monthly_listing_ts
summary(monthly_listing_ts)
autoplot(hw_fc)
summary(hw_fc)


