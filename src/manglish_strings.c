#include "global.h"
#include "manglish_strings.h"
#include "strings.h"
#include "string_util.h"

// Externs for original English text symbols
extern const u8 gText_Birch_Welcome[];
extern const u8 gText_Birch_Pokemon[];
extern const u8 gText_Birch_MainSpeech[];
extern const u8 gText_Birch_AndYouAre[];
extern const u8 gText_Birch_BoyOrGirl[];
extern const u8 gText_Birch_WhatsYourName[];
extern const u8 gText_Birch_SoItsPlayer[];
extern const u8 gText_Birch_YourePlayer[];
extern const u8 gText_Birch_AreYouReady[];

extern const u8 gText_ConfirmStarterChoice[];

extern const u8 gText_WouldYouLikeToRestYourPkmn[];
extern const u8 gText_IllTakeYourPkmn[];
extern const u8 gText_RestoredPkmnToFullHealth[];
extern const u8 gText_WeHopeToSeeYouAgain[];
extern const u8 gText_ThankYouForWaiting[];
extern const u8 gText_WeHopeToSeeYouAgain2[];
extern const u8 gText_YouWantTheUsual[];

extern const u8 gText_HowMayIServeYou[];
extern const u8 gText_PleaseComeAgain[];

extern const u8 gText_ConfirmSave[];
extern const u8 gText_AlreadySavedFile[];
extern const u8 gText_SavingDontTurnOff[];
extern const u8 gText_PlayerSavedGame[];
extern const u8 gText_SavingDontTurnOffPower[];
extern const u8 gText_SaveError[];

extern const u8 gText_WhatWillPkmnDo[];
extern const u8 gText_WhatWillPkmnDo2[];

extern const u8 gText_MenuPokedex[];
extern const u8 gText_MenuPokemon[];
extern const u8 gText_MenuBag[];
extern const u8 gText_MenuPokenav[];
extern const u8 gText_MenuSave[];
extern const u8 gText_MenuOption[];
extern const u8 gText_MenuExit[];

extern const u8 gText_Yes[];
extern const u8 gText_No[];

// Phonetic Malayalam (Manglish) Translated Strings
static const u8 sText_Manglish_Birch_Welcome[] = _("Namaskaram! Kaathu ninathinu kshamikkanam!\pPOKéMON-te lokaththekk swaagatham!\pEnte peru BIRCH.\pPakshe ellavarum enne POKéMON\nPROFESSOR ennu vilikkunnu.\p$");
static const u8 sText_Manglish_Birch_Pokemon[] = _("Ithine aanu njangal “POKéMON”\nennu vilikkunnath.\p\n$");
static const u8 sText_Manglish_Birch_MainSpeech[] = _("Ee lokam muzhuvan POKéMON enna\njeevikalal niranjiirikkunnu.\pManushyarum POKéMON-um orumich\nsahakarichu jeevikkunnu.\pChilar changathikal aayi,\nchilar jolicheyyan sahakarikkunnu.\pChila samayathu njangal orumich\nbattle-ukal nadathunnu.\pEnnalum POKéMON-e patti ellam\nnjangalkk ariyilla.\pSathtathil ithil valare valiya\nrahasyangal adangiyittund.\pEe rahasyangal kandethan aanu\nnjan research nadathunnath.\p$");
static const u8 sText_Manglish_Birch_AndYouAre[] = _("Pinne ningalude peru?$");
static const u8 sText_Manglish_Birch_BoyOrGirl[] = _("Nee aano aano?\nAthod pennano?$");
static const u8 sText_Manglish_Birch_WhatsYourName[] = _("Shari.\nNinte peru enthanu?$");
static const u8 sText_Manglish_Birch_SoItsPlayer[] = _("Ahaa, {PLAYER}{KUN} aanalle?$");
static const u8 sText_Manglish_Birch_YourePlayer[] = _("Aah, manassilayi!\pNee LITTLEROOT-ilekk thamasam\nmaari varunna {PLAYER}{KUN} alle!\nIppol karyam pidikittii!\p$");
static const u8 sText_Manglish_Birch_AreYouReady[] = _("Shari, nee ready aano?\pNinte swantham yathra ippol\narambhikkan pokukayanu.\pDhairyam aayi POKéMON lokaththekk\nchaadi irangikko!\nSwapnangalum snehavum ninte koodeyund!\pPinne, njan ninte varavum nokki\nPOKéMON LAB-il kaanum.\p$");

static const u8 sText_Manglish_ConfirmStarterChoice[] = _("Ee POKéMON-e thanne aano\nthiranjedukkunnath?");

static const u8 sText_Manglish_WouldYouLikeToRestYourPkmn[] = _("Namaskaram! POKéMON CENTER-ilekk\nswaagatham!\pNjangal ninte POKéMON-ukale\nsughappeduthi tharaam.\pPOKéMON-e rest cheyyikkano?$");
static const u8 sText_Manglish_IllTakeYourPkmn[] = _("Shari, njan ninte POKéMON-e\nkurachu neraththekk edukkukayanu.$");
static const u8 sText_Manglish_RestoredPkmnToFullHealth[] = _("Kaathu ninathinu nandi.\pNinte POKéMON-e poornnamayi\nsughappeduthiyittund.$");
static const u8 sText_Manglish_WeHopeToSeeYouAgain[] = _("Veendum kaanam! Nalla yathra\nashamsikkunnu!$");
static const u8 sText_Manglish_ThankYouForWaiting[] = _("Kaathu ninathinu nandi.$");
static const u8 sText_Manglish_YouWantTheUsual[] = _("Kandathil santhosham, {PLAYER}!\nPazhaya pole thanne cheyyatte?$");

static const u8 sText_Manglish_HowMayIServeYou[] = _("Namaskaram!\nNjangal enganeya sahayeckendiye?$");
static const u8 sText_Manglish_PleaseComeAgain[] = _("Nandi! Veendum varane!$");

static const u8 sText_Manglish_ConfirmSave[] = _("Game SAVE cheyyano?$");
static const u8 sText_Manglish_AlreadySavedFile[] = _("Munpe SAVE cheytha file und.\nAthinte mele save cheyyatte?$");
static const u8 sText_Manglish_SavingDontTurnOff[] = _("SAVE CHEYYUKAYANU…\nPOWER OFF CHEYYARUTHU.$");
static const u8 sText_Manglish_PlayerSavedGame[] = _("{PLAYER} game SAVE cheythu.$");
static const u8 sText_Manglish_SaveError[] = _("Save cheyyan pattiyilla.\pBackup memory check cheyyuka.$");

static const u8 sText_Manglish_WhatWillPkmnDo[] = _("What will\n{B_BUFF1} cheyyuka?");
static const u8 sText_Manglish_WhatWillPkmnDo2[] = _("What will\n{B_PLAYER_NAME} cheyyuka?");

static const u8 sText_Manglish_MenuBag[] = _("SANCHI (BAG)");
static const u8 sText_Manglish_MenuExit[] = _("PURATHEKK");

static const u8 sText_Manglish_Yes[] = _("ATE (YES)");
static const u8 sText_Manglish_No[] = _("ALLA (NO)");

struct ManglishTranslationEntry
{
    const u8 *original;
    const u8 *manglish;
};

static const struct ManglishTranslationEntry sManglishTranslations[] =
{
    // Birch Speech
    { gText_Birch_Welcome,               sText_Manglish_Birch_Welcome },
    { gText_Birch_Pokemon,               sText_Manglish_Birch_Pokemon },
    { gText_Birch_MainSpeech,            sText_Manglish_Birch_MainSpeech },
    { gText_Birch_AndYouAre,             sText_Manglish_Birch_AndYouAre },
    { gText_Birch_BoyOrGirl,             sText_Manglish_Birch_BoyOrGirl },
    { gText_Birch_WhatsYourName,         sText_Manglish_Birch_WhatsYourName },
    { gText_Birch_SoItsPlayer,           sText_Manglish_Birch_SoItsPlayer },
    { gText_Birch_YourePlayer,           sText_Manglish_Birch_YourePlayer },
    { gText_Birch_AreYouReady,           sText_Manglish_Birch_AreYouReady },

    // Starter Selection
    { gText_ConfirmStarterChoice,        sText_Manglish_ConfirmStarterChoice },

    // Pokemon Center Nurse
    { gText_WouldYouLikeToRestYourPkmn,  sText_Manglish_WouldYouLikeToRestYourPkmn },
    { gText_IllTakeYourPkmn,             sText_Manglish_IllTakeYourPkmn },
    { gText_RestoredPkmnToFullHealth,    sText_Manglish_RestoredPkmnToFullHealth },
    { gText_WeHopeToSeeYouAgain,         sText_Manglish_WeHopeToSeeYouAgain },
    { gText_ThankYouForWaiting,          sText_Manglish_ThankYouForWaiting },
    { gText_WeHopeToSeeYouAgain2,        sText_Manglish_WeHopeToSeeYouAgain },
    { gText_YouWantTheUsual,             sText_Manglish_YouWantTheUsual },

    // Poke Mart
    { gText_HowMayIServeYou,             sText_Manglish_HowMayIServeYou },
    { gText_PleaseComeAgain,             sText_Manglish_PleaseComeAgain },

    // Save Game
    { gText_ConfirmSave,                 sText_Manglish_ConfirmSave },
    { gText_AlreadySavedFile,            sText_Manglish_AlreadySavedFile },
    { gText_SavingDontTurnOff,           sText_Manglish_SavingDontTurnOff },
    { gText_PlayerSavedGame,             sText_Manglish_PlayerSavedGame },
    { gText_SavingDontTurnOffPower,      sText_Manglish_SavingDontTurnOff },
    { gText_SaveError,                   sText_Manglish_SaveError },

    // Battle Prompts
    { gText_WhatWillPkmnDo,              sText_Manglish_WhatWillPkmnDo },
    { gText_WhatWillPkmnDo2,             sText_Manglish_WhatWillPkmnDo2 },

    // Start Menu
    { gText_MenuBag,                     sText_Manglish_MenuBag },
    { gText_MenuExit,                    sText_Manglish_MenuExit },

    // Yes / No
    { gText_Yes,                         sText_Manglish_Yes },
    { gText_No,                          sText_Manglish_No },
};

const u8 *GetMalayalamTranslation(const u8 *original)
{
    u32 i;

    if (original == NULL)
        return original;

    // Fast pointer matching
    for (i = 0; i < ARRAY_COUNT(sManglishTranslations); i++)
    {
        if (sManglishTranslations[i].original == original)
            return sManglishTranslations[i].manglish;
    }

    return original;
}
