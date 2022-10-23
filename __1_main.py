import datetime

import __3_helpers
import __4_blick_request
import __2_variables


begin = datetime.datetime.now()

__3_helpers.start_new(__2_variables.translation_save)

archive_links = __4_blick_request.get_archive(__2_variables.archive_link_file, __2_variables.article_link_file)
content_links = __4_blick_request.prep_links(archive_links, __2_variables.content_link_file)
ready_content = __4_blick_request.prep_content(content_links, __2_variables.content_size)
solr_processed = __4_blick_request.curl_contents(ready_content, __2_variables.output_save_file)

print(solr_processed, " Dokumente wurden beladen.")

end = datetime.datetime.now()
print("fertig. Dauer: ", end-begin)


