EverGrandeCity_PokemonLeague_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EverGrandeCity_PokemonLeague_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

EverGrandeCity_PokemonLeague_1F_OnTransition:
	setrespawn HEAL_LOCATION_EVER_GRANDE_CITY_POKEMON_LEAGUE
	setflag FLAG_LANDMARK_POKEMON_LEAGUE
	call_if_unset FLAG_EVER_GRANDE_TOURNAMENT_WON, EverGrandeCity_PokemonLeague_1F_EventScript_GuardsBlockDoor
	end

EverGrandeCity_PokemonLeague_1F_EventScript_GuardsBlockDoor::
	setobjectxyperm LOCALID_LEAGUE_GUARD_1, 9, 2
	setobjectxyperm LOCALID_LEAGUE_GUARD_2, 10, 2
	return

EverGrandeCity_PokemonLeague_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_LEAGUE_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

EverGrandeCity_PokemonLeague_1F_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart EverGrandeCity_PokemonLeague_1F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
EverGrandeCity_PokemonLeague_1F_Pokemart:
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_MAX_REPEL
	pokemartlistend

EverGrandeCity_PokemonLeague_1F_EventScript_DoorGuard::
	lockall
	goto_if_set FLAG_EVER_GRANDE_TOURNAMENT_WON, EverGrandeCity_PokemonLeague_1F_EventScript_GoForth
	getplayerxy VAR_TEMP_0, VAR_TEMP_1
	call_if_ge VAR_TEMP_0, 11, EverGrandeCity_PokemonLeague_1F_EventScript_PlayerMoveToFrontFromRight
	call_if_le VAR_TEMP_0, 8, EverGrandeCity_PokemonLeague_1F_EventScript_PlayerMoveToFrontFromLeft
	message EverGrandeCity_PokemonLeague_1F_Text_MustHaveAllGymBadges
	waitmessage
	delay 80
	goto_if_unset FLAG_BADGE06_GET, EverGrandeCity_PokemonLeague_1F_EventScript_NotAllBadges
	closemessage
	msgbox EverGrandeCity_PokemonLeague_1F_Text_MustWinTournamentFirst, MSGBOX_DEFAULT
	msgbox EverGrandeCity_PokemonLeague_1F_Text_EnterTournamentArena, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, EverGrandeCity_PokemonLeague_1F_EventScript_WarpToTournament
	msgbox EverGrandeCity_PokemonLeague_1F_Text_ComeBackWhenReady, MSGBOX_DEFAULT
	releaseall
	end

EverGrandeCity_PokemonLeague_1F_EventScript_WarpToTournament::
	msgbox EverGrandeCity_PokemonLeague_1F_Text_GuideToArena, MSGBOX_DEFAULT
	closemessage
	warp MAP_BATTLE_COLOSSEUM_2P, 6, 7
	waitstate
	releaseall
	end

EverGrandeCity_PokemonLeague_1F_EventScript_PlayerMoveToFrontFromRight::
	applymovement LOCALID_PLAYER, EverGrandeCity_PokemonLeague_1F_Movement_MoveToFrontFromRight
	waitmovement 0
	return

EverGrandeCity_PokemonLeague_1F_EventScript_PlayerMoveToFrontFromLeft::
	applymovement LOCALID_PLAYER, EverGrandeCity_PokemonLeague_1F_Movement_MoveToFrontFromLeft
	waitmovement 0
	return

EverGrandeCity_PokemonLeague_1F_EventScript_NotAllBadges::
	playse SE_FAILURE
	msgbox EverGrandeCity_PokemonLeague_1F_Text_HaventObtainedAllBadges, MSGBOX_DEFAULT
	releaseall
	end

EverGrandeCity_PokemonLeague_1F_EventScript_GoForth::
	applymovement VAR_LAST_TALKED, Common_Movement_FacePlayer
	waitmovement 0
	msgbox EverGrandeCity_PokemonLeague_1F_Text_ChampionGoForth, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	releaseall
	end

EverGrandeCity_PokemonLeague_1F_Movement_MoveToFrontFromRight:
	walk_down
	walk_left
	walk_in_place_faster_up
	step_end

EverGrandeCity_PokemonLeague_1F_Movement_MoveToFrontFromLeft:
	walk_down
	walk_right
	walk_in_place_faster_up
	step_end

EverGrandeCity_PokemonLeague_1F_Movement_LeftGuardOutOfWay:
	walk_left
	walk_in_place_faster_down
	step_end

EverGrandeCity_PokemonLeague_1F_Movement_RightGuardOutOfWay:
	walk_right
	walk_in_place_faster_down
	step_end

EverGrandeCity_PokemonLeague_1F_Text_MustHaveAllGymBadges:
	.string "Beyond this point, only those TRAINERS\n"
	.string "who have collected all the GYM BADGES\l"
	.string "are permitted to enter.\p"
	.string "TRAINER, let us confirm that you have\n"
	.string "all 8 GYM BADGES...$"

EverGrandeCity_PokemonLeague_1F_Text_HaventObtainedAllBadges:
	.string "You haven't obtained all 8 BADGES.\p"
	.string "If you're bound for the EVER GRANDE\n"
	.string "CONFERENCE, you must return with them.$"

EverGrandeCity_PokemonLeague_1F_Text_MustWinTournamentFirst:
	.string "All 8 BADGES verified!\p"
	.string "Welcome, TRAINER, to the prestigious\n"
	.string "EVER GRANDE CONFERENCE!\p"
	.string "Before you may challenge the ELITE FOUR\n"
	.string "and CHAMPION WALLACE, you must prove\l"
	.string "your mastery by conquering the\l"
	.string "EVER GRANDE CONFERENCE TOURNAMENT!$"

EverGrandeCity_PokemonLeague_1F_Text_EnterTournamentArena:
	.string "Would you like to enter the\n"
	.string "TOURNAMENT ARENA now?$"

EverGrandeCity_PokemonLeague_1F_Text_ComeBackWhenReady:
	.string "Understood. Prepare your team and speak\n"
	.string "with us when you are ready to battle!$"

EverGrandeCity_PokemonLeague_1F_Text_GuideToArena:
	.string "Right this way to the TOURNAMENT ARENA!\n"
	.string "Best of luck, TRAINER!$"

EverGrandeCity_PokemonLeague_1F_Text_ChampionGoForth:
	.string "Welcome, EVER GRANDE CHAMPION {PLAYER}!\p"
	.string "The gates to the POKéMON LEAGUE are\n"
	.string "open for you!\p"
	.string "Believe in yourself and your POKéMON,\n"
	.string "and go forth to face the ELITE FOUR!$"
