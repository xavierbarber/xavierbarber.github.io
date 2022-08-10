
library(distill)
create_website(dir = "~/Dropbox/curri xavi/CV_website", 
               title = "Xavi Barber's website", 
               gh_pages = TRUE)


create_article(file = "xbarber",         # future name of .Rmd file
               template = "trestles",    # name of template
               package = "postcards") # package that includes the template

create_article(file = "moreinfo",         # future name of .Rmd file
               template = "trestles",    # name of template
               package = "postcards") # package that includes the template

create_article(file = "cva",         # future name of .Rmd file
               template = "trestles",    # name of template
               package = "postcards")