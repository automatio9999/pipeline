from curl_cffi import Session
from curl_cffi.requests import impersonate
import ua_generator
from ua_generator.options import Options
from ua_generator.data.version import VersionRange

def get_random_user_agent() -> dict:
    options = Options()
    options.version_ranges = {
        'chrome': VersionRange(140, 144),  # Choose version between 125 and 129
    }
    ua = ua_generator.generate(browser='chrome', options=options)
    ua.headers.accept_ch("Sec-CH-UA-Platform-Version, Sec-CH-UA-Full-Version-List")
    return ua.headers.get()



def new_session() -> Session:
    user_agent = get_random_user_agent()
    session = Session()
    session.headers.update(user_agent)
    return session


