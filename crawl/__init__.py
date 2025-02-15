from .yes24 import crawl_yes24_event_details
from .kyobo import crawl_kyobo_event_details
from .aladin import crawl_aladin_event_details
from .animate import crawl_animate_event_details
from .daewon import crawl_daewon_event_details
from .comiccity import crawl_comiccity_event_details

def crawl_all_events(search_query, selected_sites):
        events = []

        if "yes24" in selected_sites:
            events += crawl_yes24_event_details(search_query)
        if "kyobo" in selected_sites:
            events += crawl_kyobo_event_details(search_query)
        if "aladin" in selected_sites:
            events += crawl_aladin_event_details(search_query)
        if "animate" in selected_sites:
            events += crawl_animate_event_details(search_query)
        if "daewon" in selected_sites:
            events += crawl_daewon_event_details(search_query)
        if "comiccity" in selected_sites:
            events += crawl_comiccity_event_details(search_query)

        return events