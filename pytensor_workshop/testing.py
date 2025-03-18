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
        r"https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHk1c24wYWNieXVzbWx1b3IzYXA3MjNwNGllNGFyY3F3ZGkzbzZkMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KHJw9NRFDMom487qyo/giphy.gif",
        r"https://raw.githubusercontent.com/pymc-devs/pytensor-workshop/refs/heads/main/data/success_fail_gifs/colt_club_fail.gif",
        r"https://raw.githubusercontent.com/pymc-devs/pytensor-workshop/refs/heads/main/data/success_fail_gifs/failboat.jpeg",
    )

    SUCCESS_URLS = (
        r"https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2Y2YWZoNXYycWV0aTFhbnBsZm80bXo1MWx4NDNlZGdleGY2ZG5qayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/o75ajIFH0QnQC3nCeD/giphy.gif",
        r"https://media.giphy.com/media/37nRXpCEP9H1f1WVrb/giphy.gif?cid=790b76113f6afh5v2qeti1anplfo4mz51lx43edgexf6dnjk&ep=v1_gifs_search&rid=giphy.gif&ct=g",
        r"https://media.giphy.com/media/XreQmk7ETCak0/giphy.gif?cid=790b76113f6afh5v2qeti1anplfo4mz51lx43edgexf6dnjk&ep=v1_gifs_search&rid=giphy.gif&ct=g",
        r"https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYW05OTBmOGF4cGFiNGpram14dnVxOTZtNXh1ODdzajJycjV3aWFzdCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/IwAZ6dvvvaTtdI8SD5/giphy.gif",
        r"https://media.giphy.com/media/kyLYXonQYYfwYDIeZl/giphy.gif?cid=790b7611am990f8axpab4jkjmxvuq96m5xu87sj2rr5wiast&ep=v1_gifs_search&rid=giphy.gif&ct=g",
        r"https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWVpZ2x3ZWpqdWhxc3EzaHdzcXFxY201MHFxcXU1OWprMDFqaDJscyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ZDzSCKGed7nlS/giphy.gif",
        r"https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2Zsa294bzV3Zzg0bzgxYzQ3OGZpeHBybHU4N3ZyeXh6dmF3YjdtbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/zaqclXyLz3Uoo/giphy.gif",
        r"https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExeTlqeDZsd3FhdzJtN2Fwdm50cGg3ZGNjOTAxdTgxaTViMjhnaWZ5ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/2vA33ikUb0Qz6/giphy.gif",

        
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