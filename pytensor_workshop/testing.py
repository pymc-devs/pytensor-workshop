import traceback

from IPython.display import Image
from random import choice

def test(test_fn):
    FAILURE_URLS = (
        r"https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNWYweW8wcmZsc3M3b2R6emQ0NW1ybTVmcm1yb2pjd3MyMjB4M3poNCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/26ybwvTX4DTkwst6U/giphy.gif",
        r"https://media.giphy.com/media/y9gcCOXpNX8UfZrp0X/giphy.gif?cid=790b76115f0yo0rflss7odzzd45mrm5frmrojcws220x3zh4&ep=v1_gifs_search&rid=giphy.gif&ct=g",
        r"https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNWYweW8wcmZsc3M3b2R6emQ0NW1ybTVmcm1yb2pjd3MyMjB4M3poNCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/YTJXDIivNMPuNSMgc0/giphy.gif",
        r"https://media.giphy.com/media/3ePb1CHEjfSRhn6r3c/giphy.gif?cid=ecf05e47lh4bd51owc2fjjq6ur3ap0x6b6tzk0t8yzkh7o5v&ep=v1_gifs_search&rid=giphy.gif&ct=g",
        r"https://media.giphy.com/media/EyhliNtcgPDU5ixfHq/giphy.gif?cid=ecf05e47sl9jeb1qiwsgr40l66lh7nxtjpk7q49d0g99gmb5&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    )

    SUCCESS_URLS = (
        r"https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2Y2YWZoNXYycWV0aTFhbnBsZm80bXo1MWx4NDNlZGdleGY2ZG5qayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/o75ajIFH0QnQC3nCeD/giphy.gif",
        r"https://media.giphy.com/media/37nRXpCEP9H1f1WVrb/giphy.gif?cid=790b76113f6afh5v2qeti1anplfo4mz51lx43edgexf6dnjk&ep=v1_gifs_search&rid=giphy.gif&ct=g",
        r"https://media.giphy.com/media/XreQmk7ETCak0/giphy.gif?cid=790b76113f6afh5v2qeti1anplfo4mz51lx43edgexf6dnjk&ep=v1_gifs_search&rid=giphy.gif&ct=g",
        r"https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYW05OTBmOGF4cGFiNGpram14dnVxOTZtNXh1ODdzajJycjV3aWFzdCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/IwAZ6dvvvaTtdI8SD5/giphy.gif",
        r"https://media.giphy.com/media/kyLYXonQYYfwYDIeZl/giphy.gif?cid=790b7611am990f8axpab4jkjmxvuq96m5xu87sj2rr5wiast&ep=v1_gifs_search&rid=giphy.gif&ct=g",
        
    )
    def wrap_test(*args, **kwargs):
        try:
            test_fn(*args, **kwargs)
        except Exception as exc:
            traceback.print_exc()
            return Image(url=choice(FAILURE_URLS))
        else:
            print("Success")
            return Image(url=choice(SUCCESS_URLS))
    return wrap_test