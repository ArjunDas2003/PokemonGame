.set LOCALID_ARENA_MC, 1
.set LOCALID_ARENA_OPPONENT, 2
.set LOCALID_ARENA_ATTENDANT, 3

BattleColosseum_2P_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, BattleColosseum_2P_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleColosseum_2P_OnFrame
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, BattleColosseum_2P_OnWarp
	.byte 0

BattleColosseum_2P_OnTransition:
	call BattleColosseum_2P_EventScript_SetupOpponentGfx
	end

BattleColosseum_2P_OnWarp:
	map_script_2 VAR_TEMP_1, 0, BattleColosseum_2P_EventScript_TurnPlayerNorth
	.2byte 0

BattleColosseum_2P_EventScript_TurnPlayerNorth::
	turnobject OBJ_EVENT_ID_PLAYER, DIR_NORTH
	end

BattleColosseum_2P_EventScript_SetupOpponentGfx::
	switch VAR_EVER_GRANDE_TOURNAMENT_STAGE
	case 0, BattleColosseum_2P_EventScript_SetGfxRound1
	case 1, BattleColosseum_2P_EventScript_SetGfxRound2
	case 2, BattleColosseum_2P_EventScript_SetGfxRound3
	case 3, BattleColosseum_2P_EventScript_SetGfxRound4
	case 4, BattleColosseum_2P_EventScript_SetGfxRival
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_MAN_3
	return

BattleColosseum_2P_EventScript_SetGfxRound1::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_MAN_3
	return

BattleColosseum_2P_EventScript_SetGfxRound2::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_EXPERT_M
	return

BattleColosseum_2P_EventScript_SetGfxRound3::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_MAN_4
	return

BattleColosseum_2P_EventScript_SetGfxRound4::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_GENTLEMAN
	return

BattleColosseum_2P_EventScript_SetGfxRival::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, BattleColosseum_2P_EventScript_SetGfxMay
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	return

BattleColosseum_2P_EventScript_SetGfxMay::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	return

BattleColosseum_2P_OnFrame:
	map_script_2 VAR_TEMP_0, 0, BattleColosseum_2P_EventScript_MatchIntro
	.2byte 0

BattleColosseum_2P_EventScript_MatchIntro::
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, BattleColosseum_2P_Movement_PlayerWalkToBox
	waitmovement 0
	setvar VAR_TEMP_0, 1
	applymovement LOCALID_ARENA_MC, Common_Movement_WalkInPlaceDown
	waitmovement 0
	switch VAR_EVER_GRANDE_TOURNAMENT_STAGE
	case 0, BattleColosseum_2P_EventScript_StartRound1
	case 1, BattleColosseum_2P_EventScript_StartRound2
	case 2, BattleColosseum_2P_EventScript_StartRound3
	case 3, BattleColosseum_2P_EventScript_StartRound4
	case 4, BattleColosseum_2P_EventScript_StartFinalRival
	msgbox BattleColosseum_2P_Text_TournamentAlreadyWon, MSGBOX_DEFAULT
	releaseall
	end

BattleColosseum_2P_EventScript_StartRound1::
	playse SE_M_ENCORE2
	msgbox BattleColosseum_2P_Text_AnnounceRound1, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ARENA_OPPONENT, Common_Movement_WalkInPlaceLeft
	waitmovement 0
	msgbox BattleColosseum_2P_Text_Round1Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_EVER_GRANDE_ROUND_1, BattleColosseum_2P_Text_Round1Defeat
	goto BattleColosseum_2P_EventScript_MatchWon
	end

BattleColosseum_2P_EventScript_StartRound2::
	playse SE_M_ENCORE2
	msgbox BattleColosseum_2P_Text_AnnounceRound2, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ARENA_OPPONENT, Common_Movement_WalkInPlaceLeft
	waitmovement 0
	msgbox BattleColosseum_2P_Text_Round2Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_EVER_GRANDE_ROUND_2, BattleColosseum_2P_Text_Round2Defeat
	goto BattleColosseum_2P_EventScript_MatchWon
	end

BattleColosseum_2P_EventScript_StartRound3::
	playse SE_M_ENCORE2
	msgbox BattleColosseum_2P_Text_AnnounceRound3, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ARENA_OPPONENT, Common_Movement_WalkInPlaceLeft
	waitmovement 0
	msgbox BattleColosseum_2P_Text_Round3Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_EVER_GRANDE_ROUND_3, BattleColosseum_2P_Text_Round3Defeat
	goto BattleColosseum_2P_EventScript_MatchWon
	end

BattleColosseum_2P_EventScript_StartRound4::
	playse SE_M_ENCORE2
	msgbox BattleColosseum_2P_Text_AnnounceRound4, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ARENA_OPPONENT, Common_Movement_WalkInPlaceLeft
	waitmovement 0
	msgbox BattleColosseum_2P_Text_Round4Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_EVER_GRANDE_ROUND_4, BattleColosseum_2P_Text_Round4Defeat
	goto BattleColosseum_2P_EventScript_MatchWon
	end

BattleColosseum_2P_EventScript_StartFinalRival::
	playse SE_M_ENCORE2
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, BattleColosseum_2P_EventScript_AnnounceFinalMay
	msgbox BattleColosseum_2P_Text_AnnounceFinalBrendan, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ARENA_OPPONENT, Common_Movement_WalkInPlaceLeft
	waitmovement 0
	msgbox BattleColosseum_2P_Text_BrendanFinalIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_EVER_GRANDE_FINAL_BRENDAN, BattleColosseum_2P_Text_BrendanFinalDefeat
	goto BattleColosseum_2P_EventScript_MatchWon
	end

BattleColosseum_2P_EventScript_AnnounceFinalMay::
	msgbox BattleColosseum_2P_Text_AnnounceFinalMay, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ARENA_OPPONENT, Common_Movement_WalkInPlaceLeft
	waitmovement 0
	msgbox BattleColosseum_2P_Text_MayFinalIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_EVER_GRANDE_FINAL_MAY, BattleColosseum_2P_Text_MayFinalDefeat
	goto BattleColosseum_2P_EventScript_MatchWon
	end

BattleColosseum_2P_EventScript_MatchWon::
	playse SE_M_ENCORE2
	special HealPlayerParty
	addvar VAR_EVER_GRANDE_TOURNAMENT_STAGE, 1
	goto_if_ge VAR_EVER_GRANDE_TOURNAMENT_STAGE, 5, BattleColosseum_2P_EventScript_TournamentChampionWon
	msgbox BattleColosseum_2P_Text_AdvanceToNextRound, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, BattleColosseum_2P_EventScript_ProceedNextRound
	msgbox BattleColosseum_2P_Text_TakeRestInLobby, MSGBOX_DEFAULT
	closemessage
	warp MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F, 9, 5
	waitstate
	releaseall
	end

BattleColosseum_2P_EventScript_ProceedNextRound::
	setvar VAR_TEMP_0, 0
	warp MAP_BATTLE_COLOSSEUM_2P, 6, 7
	waitstate
	releaseall
	end

BattleColosseum_2P_EventScript_TournamentChampionWon::
	playfanfare MUS_OBTAIN_BADGE
	msgbox BattleColosseum_2P_Text_CrownChampion, MSGBOX_DEFAULT
	waitfanfare
	setflag FLAG_EVER_GRANDE_TOURNAMENT_WON
	msgbox BattleColosseum_2P_Text_ChampionAccessUnlocked, MSGBOX_DEFAULT
	closemessage
	warp MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F, 9, 5
	waitstate
	releaseall
	end

BattleColosseum_2P_EventScript_MC::
	lock
	faceplayer
	goto_if_set FLAG_EVER_GRANDE_TOURNAMENT_WON, BattleColosseum_2P_EventScript_MCPraisChampion
	msgbox BattleColosseum_2P_Text_MCGeneralSpeech, MSGBOX_DEFAULT
	release
	end

BattleColosseum_2P_EventScript_MCPraisChampion::
	msgbox BattleColosseum_2P_Text_MCPraisChampion, MSGBOX_DEFAULT
	release
	end

BattleColosseum_2P_EventScript_Opponent::
	lock
	faceplayer
	msgbox BattleColosseum_2P_Text_OpponentWaiting, MSGBOX_DEFAULT
	release
	end

BattleColosseum_2P_EventScript_Attendant::
	lock
	faceplayer
	special HealPlayerParty
	playse SE_USE_ITEM
	msgbox BattleColosseum_2P_Text_AttendantHealed, MSGBOX_DEFAULT
	msgbox BattleColosseum_2P_Text_AttendantAskLeave, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, BattleColosseum_2P_EventScript_AttendantWarpOut
	release
	end

BattleColosseum_2P_EventScript_AttendantWarpOut::
	msgbox BattleColosseum_2P_Text_ReturningToLobby, MSGBOX_DEFAULT
	closemessage
	warp MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F, 9, 5
	waitstate
	release
	end

BattleColosseum_2P_Movement_PlayerWalkToBox:
	walk_up
	walk_up
	walk_left
	walk_left
	walk_in_place_faster_right
	step_end

BattleColosseum_2P_Text_AnnounceRound1:
	.string "REFEREE: Welcome to the EVER GRANDE\n"
	.string "CONFERENCE TOURNAMENT!\p"
	.string "GROUP STAGE: MATCH 1 - 3-on-3 Battle!\n"
	.string "{PLAYER} versus ACE TRAINER KAITO!\p"
	.string "Trainers, bring forth your POKéMON!$"

BattleColosseum_2P_Text_Round1Intro:
	.string "KAITO: I fought my way through all 8\n"
	.string "GYMS to stand in this arena!\p"
	.string "Show me what you've got!$"

BattleColosseum_2P_Text_Round1Defeat:
	.string "Incredible skill... You earned this win!$"

BattleColosseum_2P_Text_AnnounceRound2:
	.string "REFEREE: Welcome back to the arena!\p"
	.string "GROUP STAGE: MATCH 2 - 3-on-3 Battle!\n"
	.string "{PLAYER} versus EXPERT HIROSHI!\p"
	.string "Let the battle commence!$"

BattleColosseum_2P_Text_Round2Intro:
	.string "HIROSHI: Decades of experience will\n"
	.string "test your bond with your POKéMON!$"

BattleColosseum_2P_Text_Round2Defeat:
	.string "Magnificent! A true master in the making!$"

BattleColosseum_2P_Text_AnnounceRound3:
	.string "REFEREE: The Group Stage has concluded!\p"
	.string "Welcome to the KNOCKOUT QUARTER-FINALS!\n"
	.string "Full 6-on-6 Single Battle!\p"
	.string "{PLAYER} versus DRAGON TAMER RYUTO!$"

BattleColosseum_2P_Text_Round3Intro:
	.string "RYUTO: Feel the overwhelming might of\n"
	.string "my ferocious dragons and steel titans!$"

BattleColosseum_2P_Text_Round3Defeat:
	.string "My dragons were outmatched! Fantastic!$"

BattleColosseum_2P_Text_AnnounceRound4:
	.string "REFEREE: The tension is electrifying!\p"
	.string "This is the KNOCKOUT SEMI-FINALS!\n"
	.string "Full 6-on-6 Single Battle!\p"
	.string "{PLAYER} versus VETERAN JON!\p"
	.string "Winner advances to the GRAND FINALS!$"

BattleColosseum_2P_Text_Round4Intro:
	.string "JON: Only one of us can face the\n"
	.string "Finalist! I won't hold anything back!$"

BattleColosseum_2P_Text_Round4Defeat:
	.string "You are unstoppable! Go on and win it all!$"

BattleColosseum_2P_Text_AnnounceFinalBrendan:
	.string "REFEREE: LADIES AND GENTLEMEN!\n"
	.string "Welcome to the EVER GRANDE GRAND FINALS!\p"
	.string "Full 6-on-6 Championship Battle!\p"
	.string "In the red corner: {PLAYER}!\n"
	.string "In the blue corner: BRENDAN!\p"
	.string "Two rivals clashing for the crown of HOENN!\n"
	.string "BATTLE BEGIN!$"

BattleColosseum_2P_Text_BrendanFinalIntro:
	.string "BRENDAN: {PLAYER}!\n"
	.string "Ever since Route 103, we've pushed\l"
	.string "each other every step of the journey!\p"
	.string "My 6-POKéMON team is at its peak!\n"
	.string "Let's see who truly is the strongest!$"

BattleColosseum_2P_Text_BrendanFinalDefeat:
	.string "Whoa... You really are the best,\n"
	.string "{PLAYER}! What an unforgettable match!$"

BattleColosseum_2P_Text_AnnounceFinalMay:
	.string "REFEREE: LADIES AND GENTLEMEN!\n"
	.string "Welcome to the EVER GRANDE GRAND FINALS!\p"
	.string "Full 6-on-6 Championship Battle!\p"
	.string "In the red corner: {PLAYER}!\n"
	.string "In the blue corner: MAY!\p"
	.string "Two rivals clashing for the crown of HOENN!\n"
	.string "BATTLE BEGIN!$"

BattleColosseum_2P_Text_MayFinalIntro:
	.string "MAY: {PLAYER}!\n"
	.string "From our first battle to this grand stage,\l"
	.string "I've been preparing for this exact moment!\p"
	.string "My 6-POKéMON team is ready!\n"
	.string "Let's make this the battle of a lifetime!$"

BattleColosseum_2P_Text_MayFinalDefeat:
	.string "Aww, you did it, {PLAYER}!\n"
	.string "You're truly the greatest trainer!$"

BattleColosseum_2P_Text_AdvanceToNextRound:
	.string "REFEREE: {PLAYER} wins the match!\n"
	.string "Your team has been fully restored!\p"
	.string "Would you like to proceed immediately\n"
	.string "to the next tournament match?$"

BattleColosseum_2P_Text_TakeRestInLobby:
	.string "REFEREE: Understood! Take your time to\n"
	.string "rest and prepare in the League Lobby!$"

BattleColosseum_2P_Text_CrownChampion:
	.string "REFEREE: LADIES AND GENTLEMEN!\n"
	.string "WE HAVE OUR NEW EVER GRANDE CHAMPION!\p"
	.string "{PLAYER} HAS WON THE HOENN CONFERENCE!$"

BattleColosseum_2P_Text_ChampionAccessUnlocked:
	.string "REFEREE: As the Conference Champion,\n"
	.string "the gates to the POKéMON LEAGUE are\l"
	.string "now officially unlocked for you!\p"
	.string "Go forth and challenge the ELITE FOUR\n"
	.string "and CHAMPION WALLACE!$"

BattleColosseum_2P_Text_TournamentAlreadyWon:
	.string "REFEREE: Congratulations, CHAMPION {PLAYER}!\n"
	.string "The ELITE FOUR awaits your challenge!$"

BattleColosseum_2P_Text_MCGeneralSpeech:
	.string "MC: The EVER GRANDE CONFERENCE showcases\n"
	.string "the finest trainers from across HOENN!$"

BattleColosseum_2P_Text_MCPraisChampion:
	.string "MC: All hail the new Conference Champion,\n"
	.string "{PLAYER}! A legendary victory!$"

BattleColosseum_2P_Text_OpponentWaiting:
	.string "The opponent is focusing intensely on\n"
	.string "the upcoming match.$"

BattleColosseum_2P_Text_AttendantHealed:
	.string "ATTENDANT: Your POKéMON have been\n"
	.string "fully restored to peak health!$"

BattleColosseum_2P_Text_AttendantAskLeave:
	.string "Would you like to return to the\n"
	.string "POKéMON LEAGUE lobby?$"

BattleColosseum_2P_Text_ReturningToLobby:
	.string "ATTENDANT: Best of luck, TRAINER!$"
