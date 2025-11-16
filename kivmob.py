from kivy.core.window import Window
from kivy.logger import Logger
from kivy.metrics import dp
from kivy.utils import platform

if platform == "android":
    try:
        from jnius import autoclass, cast, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread

        activity = autoclass("org.kivy.android.PythonActivity")
        AdListener = autoclass("com.google.android.gms.ads.AdListener")
        AdMobAdapter = autoclass("com.google.ads.mediation.admob.AdMobAdapter")
        AdRequest = autoclass("com.google.android.gms.ads.AdRequest")
        AdRequestBuilder = autoclass("com.google.android.gms.ads.AdRequest$Builder")
        AdSize = autoclass("com.google.android.gms.ads.AdSize")
        AdView = autoclass("com.google.android.gms.ads.AdView")
        Bundle = autoclass("android.os.Bundle")
        Gravity = autoclass("android.view.Gravity")
        InterstitialAd = autoclass("com.google.android.gms.ads.interstitial.InterstitialAd")
        LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")
        LinearLayout = autoclass("android.widget.LinearLayout")
        MobileAds = autoclass("com.google.android.gms.ads.MobileAds")
        RewardItem = autoclass("com.google.android.gms.ads.rewarded.RewardItem")
        View = autoclass("android.view.View")
    
    except BaseException:
        Logger.error(
            "KivMob: Cannot load AdMob classes. Check buildozer.spec."
        )

else:

    """
    class AdMobRewardedVideoAdListener:
        pass
    """

    def run_on_ui_thread(x):
        pass

class TestIds:
    """ Enum of test ad ids provided by AdMob. This allows developers to
        test displaying ads without setting up an AdMob account.
    """

    """ Test AdMob App ID """
    APP = "ca-app-pub-3940256099942544~3347511713"

    """ Test Banner Ad ID """
    BANNER = "ca-app-pub-3940256099942544/6300978111"

    """ Test Interstitial Ad ID """
    INTERSTITIAL = "ca-app-pub-3940256099942544/1033173712"

    """ Test Interstitial Video Ad ID """
    INTERSTITIAL_VIDEO = "ca-app-pub-3940256099942544/8691691433"

    """ Test Rewarded Video Ad ID """
    REWARDED_VIDEO = "ca-app-pub-3940256099942544/5224354917"

class AdMobBridge:
    def __init__(self, appID):
        pass

    def add_test_device(self, testID):
        pass

    def is_interstitial_loaded(self):
        return False

    def new_banner(self, unitID, top_pos=True):
        pass

    def new_interstitial(self, unitID):
        pass

    def request_banner(self, options):
        pass

    def request_interstitial(self, options):
        pass

    def show_banner(self):
        pass

    def show_interstitial(self):
        pass

    def destroy_banner(self):
        pass

    def destroy_interstitial(self):
        pass

    def hide_banner(self):
        pass

    def set_rewarded_ad_listener(self, listener):
        pass

    def load_rewarded_ad(self, unitID):
        pass

    def show_rewarded_ad(self):
        pass

class InterstitialAdLoadListener(PythonJavaClass):
    __javaclass__ = 'com/google/android/gms/ads/interstitial/InterstitialAdLoadCallback'
    __javainterfaces__ = ['com/google/android/gms/ads/interstitial/InterstitialAdLoadCallback']

    def __init__(self):
        super(InterstitialAdLoadListener, self).__init__()
        self.interstitial_ad = None

    @java_method('(Lcom/google/android/gms/ads/interstitial/InterstitialAd;)V')
    def onAdLoaded(self, ad):
        print("Ad was loaded successfully!")
        self.interstitial_ad = cast('com.google.android.gms.ads.interstitial.InterstitialAd', ad)

    @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
    def onAdFailedToLoad(self, adError):
        print(f"Ad failed to load: {adError.toString()}")
        self.interstitial_ad = None
    

class AndroidBridge(AdMobBridge):
    @run_on_ui_thread
    def __init__(self, appID):
        self._loaded = False

        try:
            MobileAds.initialize(activity.mActivity)

        except ValueError as error:
            print(error)
            
        try:
            if activity == None:
                print("Error: activity is None")
            if activity.mActivity == None:
                print("Error: activity.mActivity is None")
            print("activity -> ", activity)
            print("activity.mActivity -> ", activity.mActivity)
            self.inter_listener = InterstitialAdLoadListener()
            self.inter_id = None
            self._interstitial = None

            self._adview = AdView(activity.mActivity)
            #self._interstitial = InterstitialAd(activity.mActivity)
            self._rewarded = MobileAds.getRewardedVideoAdInstance(
                activity.mActivity
            )
        except Exception as e:
            print("Exception Raised in the block _adview, _interstitial, _rewarded: ", e)
        self._test_devices = []

    @run_on_ui_thread
    def add_test_device(self, testID):
        self._test_devices.append(testID)

    @run_on_ui_thread
    def new_banner(self, unitID, top_pos=True):
        self._adview = AdView(activity.mActivity)
        self._adview.setAdUnitId(unitID)
        self._adview.setAdSize(AdSize.SMART_BANNER)
        self._adview.setVisibility(View.GONE)
        adLayoutParams = LayoutParams(
            LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT
        )
        self._adview.setLayoutParams(adLayoutParams)
        layout = LinearLayout(activity.mActivity)
        if not top_pos:
            layout.setGravity(Gravity.BOTTOM)
        layout.addView(self._adview)
        layoutParams = LayoutParams(
            LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT
        )
        layout.setLayoutParams(layoutParams)
        activity.mActivity.addContentView(layout, layoutParams)

    @run_on_ui_thread
    def request_banner(self, options={}):
        self._adview.loadAd(self._get_builder(options).build())

    @run_on_ui_thread
    def show_banner(self):
        self._adview.setVisibility(View.VISIBLE)

    @run_on_ui_thread
    def hide_banner(self):
        self._adview.setVisibility(View.GONE)

    @run_on_ui_thread
    def new_interstitial(self, unitID):
        #self._interstitial.setAdUnitId(unitID)
        self.inter_id = unitID

    @run_on_ui_thread
    def request_interstitial(self, options={}):
        #self._interstitial.loadAd(self._get_builder(options).build())
        if self.inter_id is not None:
            InterstitialAd.load(activity.mActivity, self.inter_id, self._get_builder(options).build(), self.inter_listener)
        else:
            print("No ID for interstitial ad.")

    @run_on_ui_thread
    def _is_interstitial_loaded(self):
        #self._loaded = self._interstitial.isLoaded()
        self._loaded = True if self.inter_listener.interstitial_ad is not None else False

    def is_interstitial_loaded(self):
        self._is_interstitial_loaded()
        return self._loaded

    @run_on_ui_thread
    def show_interstitial(self):
        #if self.is_interstitial_loaded():
        #    self._interstitial.show()
        if self.inter_listener.interstitial_ad:
            self.inter_listener.interstitial_ad.show(activity.mActivity)
        else:
            print("Ad not ready to show.")

    @run_on_ui_thread
    def set_rewarded_ad_listener(self, listener):
        self._listener = AdMobRewardedVideoAdListener(listener)
        self._rewarded.setRewardedVideoAdListener(self._listener)

    @run_on_ui_thread
    def load_rewarded_ad(self, unitID):
        builder = self._get_builder(None)
        self._rewarded.loadAd(unitID, builder.build())

    @run_on_ui_thread
    def show_rewarded_ad(self):
        if self._rewarded.isLoaded():
            self._rewarded.show()

    @run_on_ui_thread
    def destroy_banner(self):
        self._adview.destroy()

    @run_on_ui_thread
    def destroy_interstitial(self):
        self._interstitial.destroy()

    @run_on_ui_thread
    def destroy_rewarded_video_ad(self):
        self._rewarded.destroy()

    def _get_builder(self, options):
        builder = AdRequestBuilder()
        if options is not None:
            if "children" in options:
                builder.tagForChildDirectedTreatment(options["children"])
            if "family" in options:
                extras = Bundle()
                extras.putBoolean(
                    "is_designed_for_families", options["family"]
                )
                builder.addNetworkExtrasBundle(AdMobAdapter, extras)
        
        for test_device in self._test_devices:
            if len(self._test_devices) != 0:
                builder.addTestDevice(test_device)
                
        return builder

class iOSBridge(AdMobBridge):
    # TODO
    pass


class KivMob:
    """ Allows access to AdMob functionality on Android devices.
    """

    def __init__(self, appID):
        Logger.info("KivMob: __init__ called.")
        self._banner_top_pos = True
        if platform == "android":
            Logger.info("KivMob: Android platform detected.")
            self.bridge = AndroidBridge(appID)
        elif platform == "ios":
            Logger.warning("KivMob: iOS not yet supported.")
            self.bridge = iOSBridge(appID)
        else:
            Logger.warning("KivMob: Ads will not be shown.")
            self.bridge = AdMobBridge(appID)

    def add_test_device(self, device):
        """ Add test device ID, which will trigger test ads to be displayed on
            that device

            :type device: string
            :param device: The test device ID of the Android device.
        """
        Logger.info("KivMob: add_test_device() called.")
        self.bridge.add_test_device(device)

    def new_banner(self, unitID, top_pos=True):
        """ Create a new mobile banner ad.

            :type unitID: string
            :param unitID: AdMob banner ID for mobile application.
            :type top_pos: boolean
            :param top_pos: Positions banner at the top of the page if True,
            bottom if otherwise.
        """
        Logger.info("KivMob: new_banner() called.")
        self.bridge.new_banner(unitID, top_pos)

    def new_interstitial(self, unitID):
        """ Create a new mobile interstitial ad.

            :type unitID: string
            :param unitID: AdMob interstitial ID for mobile application.
        """
        Logger.info("KivMob: new_interstitial() called.")
        self.bridge.new_interstitial(unitID)

    def is_interstitial_loaded(self):
        """ Check if the interstitial ad has loaded.
        """
        Logger.info("KivMob: is_interstitial_loaded() called.")
        return self.bridge.is_interstitial_loaded()

    def request_banner(self, options={}):
        """ Request a new banner ad from AdMob.
        """
        Logger.info("KivMob: request_banner() called.")
        self.bridge.request_banner(options)

    def request_interstitial(self, options={}):
        """ Request a new interstitial ad from AdMob.
        """
        Logger.info("KivMob: request_interstitial() called.")
        self.bridge.request_interstitial(options)

    def show_banner(self):
        """ Displays banner ad, if it has loaded.
        """
        Logger.info("KivMob: show_banner() called.")
        self.bridge.show_banner()

    def show_interstitial(self):
        """ Displays interstitial ad, if it has loaded.
        """
        Logger.info("KivMob: show_interstitial() called.")
        self.bridge.show_interstitial()

    def destroy_banner(self):
        """ Destroys current banner ad.
        """
        Logger.info("KivMob: destroy_banner() called.")
        self.bridge.destroy_banner()

    def destroy_interstitial(self):
        """ Destroys current interstitial ad.
        """
        Logger.info("KivMob: destroy_interstitial() called.")
        self.bridge.destroy_interstitial()

    def hide_banner(self):
        """  Hide current banner ad.
        """
        Logger.info("KivMob: hide_banner() called.")
        self.bridge.hide_banner()

    def set_rewarded_ad_listener(self, listener):
        """ Set listener object for rewarded video ads.

            :type listener: AdMobRewardedVideoAdListener
            :param listener: Handles callback functionality for
            rewarded video ads.
        """
        Logger.info("KivMob: set_rewarded_ad_listener() called.")
        self.bridge.set_rewarded_ad_listener(listener)

    def load_rewarded_ad(self, unitID):
        """ Load rewarded video ad.

            :type unitID: string
            :param unitID: AdMob rewarded video ID for mobile application.
        """
        Logger.info("KivMob: load_rewarded_ad() called.")
        self.bridge.load_rewarded_ad(unitID)

    def show_rewarded_ad(self):
        """ Display rewarded video ad.
        """
        Logger.info("KivMob: show_rewarded_ad() called.")
        self.bridge.show_rewarded_ad()

    def determine_banner_height(self):
        """ Utility function for determining the height (dp) of the banner ad.

            :return height: Height of banner ad in dp.
        """
        height = dp(32)
        upper_bound = dp(720)
        if Window.height > upper_bound:
            height = dp(90)
        elif dp(400) < Window.height <= upper_bound:
            height = dp(50)
        return height


if __name__ == "__main__":
    print(
        "\033[92m  _  ___       __  __       _\n"
        " | |/ (_)_   _|  \\/  | ___ | |__\n"
        " | ' /| \\ \\ / / |\\/| |/ _ \\| '_ \\\n"
        " | . \\| |\\ V /| |  | | (_) | |_) |\n"
        " |_|\\_\\_| \\_/ |_|  |_|\\___/|_.__/\n\033[0m"
    )
    print(" AdMob support for Kivy\n")
    print(" Michael Stott, 2019\n")