library(sf)
library(tidyverse)

ptdf = read_delim('coast.txt', delim = ' ', col_names = c('x', 'y', 'z'), skip = 1)

outer = ptdf %>% 
  filter(row_number() < 5963) %>% 
  select(x, y) %>% 
  bind_rows(.[1,]) %>% 
  as.matrix()

inner = ptdf %>% 
  filter(row_number() >= 5963) %>% 
  select(x, y) %>% 
  bind_rows(.[1,]) %>% 
  as.matrix()

sea = st_polygon(list(inner, outer)) %>% 
  st_sfc(crs = 4326)

write_sf(sea, 'data/sea.shp')
