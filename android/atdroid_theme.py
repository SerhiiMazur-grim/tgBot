import os

from config.alfa_bg import alfa_bg


async def color_to_int32(color):
    if len(color) == 7:
        color = f'#ff{color[1:]}'

    color = int(color[1:], 16)
    # Розділяємо колір на компоненти: альфа, червоний, зелений і синій.
    alpha = (color >> 24) & 0xFF
    red = (color >> 16) & 0xFF
    green = (color >> 8) & 0xFF
    blue = color & 0xFF

    # Перевіряємо, чи найстарший біт (знаковий біт) альфа-каналу встановлений.
    if alpha & 0x80:
        # Якщо так, то ми маємо справу з від'ємним числом.
        # Обчислюємо від'ємне значення залишкового біту.
        alpha = alpha - 256

    # Повертаємо 32-бітне число зі знаком, де біти розміщені так: AARRGGBB.
    return (alpha << 24) | (red << 16) | (green << 8) | blue


async def img_to_binar(image_path):
    with open(image_path, 'rb') as file:
        binary_data = file.read()
    return binary_data


async def adjust_color_brightness(hex_color, factor=0.1):
    # Перетворюємо рядок у форматі "#RRGGBB" у відповідне ціле число.
    color = int(hex_color[1:], 16)

    # Розділяємо колір на компоненти: червоний, зелений і синій.
    red = (color >> 16) & 0xFF
    green = (color >> 8) & 0xFF
    blue = color & 0xFF

    # Обчислюємо інтенсивність коліру. Ми використовуємо середню інтенсивність RGB.
    brightness = (red + green + blue) / 3.0

    # Визначаємо, чи колір є світлим чи темним, використовуючи порігове значення 128.
    if brightness < 128:
        # Колір темний, отже, ми освітлюємо його на заданий коефіцієнт.
        new_red = int(red + (255 - red) * factor)
        new_green = int(green + (255 - green) * factor)
        new_blue = int(blue + (255 - blue) * factor)
    else:
        # Колір світлий, отже, ми затемнюємо його на заданий коефіцієнт.
        new_red = int(red * (1 - factor))
        new_green = int(green * (1 - factor))
        new_blue = int(blue * (1 - factor))

    # Запобігаємо виходу за межі 0-255 для кожного компонента.
    new_red = max(0, min(255, new_red))
    new_green = max(0, min(255, new_green))
    new_blue = max(0, min(255, new_blue))

    # Формуємо новий колір у форматі "#RRGGBB" і повертаємо його.
    new_color = "#{:02X}{:02X}{:02X}".format(new_red, new_green, new_blue)
    return new_color


async def create_android_theme(chat_id, image_path, bg, primary_txt, secondary_txt, alfa):
    alfa = alfa_bg[alfa]
    bg_hex = bg
    file_name = f'{bg}{primary_txt}{secondary_txt}.attheme'
    binar_imag = await img_to_binar(image_path)
    bg = await color_to_int32(bg)
    primary_txt = await color_to_int32(primary_txt)
    secondary_txt = await color_to_int32(secondary_txt)
    chat_in = await adjust_color_brightness(bg_hex)
    chat_in_bubble = await color_to_int32(f'#{alfa}{chat_in[1:]}')
    chat_out_bubble = await color_to_int32(f'#{alfa}{bg_hex[1:]}')
    ikb_bg = await color_to_int32(f'#{alfa}{chat_in[1:]}')

    data = [
        f'actionBarActionModeDefault={bg}',
        f'actionBarActionModeDefaultIcon={primary_txt}',
        f'actionBarActionModeDefaultSelector={primary_txt}',
        f'actionBarActionModeDefaultTop={bg}',
        f'actionBarDefault={bg}',
        f'actionBarDefaultArchived={bg}',
        f'actionBarDefaultArchivedIcon={primary_txt}',
        f'actionBarDefaultArchivedSearch={primary_txt}',
        f'actionBarDefaultArchivedSelector={primary_txt}',
        f'actionBarDefaultArchivedTitle={primary_txt}',
        f'actionBarDefaultIcon={primary_txt}',
        f'actionBarDefaultSearch={primary_txt}',
        f'actionBarDefaultSearchArchivedPlaceholder={primary_txt}',
        f'actionBarDefaultSearchPlaceholder={primary_txt}',
        f'actionBarDefaultSelector={primary_txt}',
        f'actionBarDefaultSubmenuBackground={bg}',
        f'actionBarDefaultSubmenuItem={primary_txt}',
        f'actionBarDefaultSubtitle={primary_txt}',
        f'actionBarDefaultTitle={primary_txt}',
        f'actionBarWhiteSelector={secondary_txt}',
        f'avatar_actionBarIconBlue={primary_txt}',
        f'avatar_actionBarIconCyan={primary_txt}',
        f'avatar_actionBarIconGreen={primary_txt}',
        f'avatar_actionBarIconOrange={primary_txt}',
        f'avatar_actionBarIconPink={primary_txt}',
        f'avatar_actionBarIconRed={primary_txt}',
        f'avatar_actionBarIconViolet={primary_txt}',
        f'avatar_actionBarSelectorBlue={primary_txt}',
        f'avatar_actionBarSelectorCyan={primary_txt}',
        f'avatar_actionBarSelectorGreen={primary_txt}',
        f'avatar_actionBarSelectorOrange={primary_txt}',
        f'avatar_actionBarSelectorPink={primary_txt}',
        f'avatar_actionBarSelectorRed={primary_txt}',
        f'avatar_actionBarSelectorViolet={primary_txt}',
        f'avatar_backgroundActionBarBlue={bg}',
        f'avatar_backgroundActionBarCyan={bg}',
        f'avatar_backgroundActionBarGreen={bg}',
        f'avatar_backgroundActionBarOrange={bg}',
        f'avatar_backgroundActionBarPink={bg}',
        f'avatar_backgroundActionBarRed={bg}',
        f'avatar_backgroundActionBarViolet={bg}',
        f'avatar_backgroundArchived={primary_txt}',
        f'avatar_backgroundArchivedHidden={primary_txt}',
        
        f'avatar_backgroundBlue={chat_in}',
        f'avatar_background2Blue={secondary_txt}',
        f'avatar_backgroundBlueShadow={secondary_txt}',
        f'avatar_backgroundCyan={chat_in}',
        f'avatar_background2Cyan={secondary_txt}',
        f'avatar_backgroundCyanShadow={secondary_txt}',
        f'avatar_backgroundGreen={chat_in}',
        f'avatar_background2Green={secondary_txt}',
        f'avatar_backgroundGreenShadow={secondary_txt}',
        'avatar_backgroundGroupCreateSpanBlue=-1261655605',
        f'avatar_backgroundInProfileBlue={secondary_txt}',
        f'avatar_backgroundInProfileCyan={secondary_txt}',
        f'avatar_backgroundInProfileGreen={secondary_txt}',
        f'avatar_backgroundInProfileOrange={secondary_txt}',
        f'avatar_backgroundInProfilePink={secondary_txt}',
        f'avatar_backgroundInProfileRed={secondary_txt}',
        f'avatar_backgroundInProfileViolet={secondary_txt}',
        f'avatar_backgroundOrange={chat_in}',
        f'avatar_background2Orange={secondary_txt}',
        f'avatar_backgroundOrangeShadow={secondary_txt}',
        f'avatar_backgroundPink={chat_in}',
        f'avatar_background2Pink={secondary_txt}',
        f'avatar_backgroundRed={chat_in}',
        f'avatar_background2Red={secondary_txt}',
        f'avatar_backgroundRedShadow={secondary_txt}',
        f'avatar_backgroundSaved={chat_in}',
        f'avatar_background2Saved={secondary_txt}',
        f'avatar_backgroundViolet={chat_in}',
        f'avatar_background2Violet={secondary_txt}',
        f'avatar_backgroundVioletShadow={secondary_txt}',
        
        f'avatar_nameInMessageBlue={primary_txt}',
        f'avatar_nameInMessageCyan={primary_txt}',
        f'avatar_nameInMessageGreen={primary_txt}',
        f'avatar_nameInMessageOrange={primary_txt}',
        f'avatar_nameInMessagePink={primary_txt}',
        f'avatar_nameInMessageRed={primary_txt}',
        f'avatar_nameInMessageViolet={primary_txt}',
        f'avatar_subtitleInProfileBlue={primary_txt}',
        f'avatar_subtitleInProfileCyan={primary_txt}',
        f'avatar_subtitleInProfileGreen={primary_txt}',
        f'avatar_subtitleInProfileOrange={primary_txt}',
        f'avatar_subtitleInProfilePink={primary_txt}',
        f'avatar_subtitleInProfileRed={primary_txt}',
        f'avatar_subtitleInProfileViolet={primary_txt}',
        f'avatar_text={primary_txt}',
        f'calls_callReceivedGreenIcon={primary_txt}',
        f'calls_callReceivedRedIcon={primary_txt}',
        f'changephoneinfo_image={secondary_txt}',
        f'chat_addContact={primary_txt}',
        f'chat_adminSelectedText={primary_txt}',
        f'chat_adminText={primary_txt}',
        f'chat_attachAudioBackground={secondary_txt}',
        f'chat_attachAudioIcon={bg}',
        f'chat_attachCameraIcon1={secondary_txt}',
        f'chat_attachCameraIcon2={secondary_txt}',
        f'chat_attachCameraIcon3={secondary_txt}',
        f'chat_attachCameraIcon4={secondary_txt}',
        f'chat_attachCameraIcon5={secondary_txt}',
        f'chat_attachCameraIcon6={secondary_txt}',
        f'chat_attachContactBackground={secondary_txt}',
        f'chat_attachContactIcon={bg}',
        f'chat_attachFileBackground={secondary_txt}',
        f'chat_attachFileIcon={bg}',
        f'chat_attachGalleryBackground={secondary_txt}',
        f'chat_attachGalleryIcon={bg}',
        f'chat_attachHideBackground={secondary_txt}',
        f'chat_attachHideIcon={bg}',
        f'chat_attachLocationBackground={secondary_txt}',
        f'chat_attachLocationIcon={bg}',
        f'chat_attachMediaBanBackground={secondary_txt}',
        f'chat_attachMediaBanText={bg}',
        f'chat_attachSendBackground={secondary_txt}',
        f'chat_attachSendIcon={bg}',
        f'chat_attachVideoBackground={secondary_txt}',
        f'chat_attachVideoIcon={bg}',
        f'chat_botButtonText={primary_txt}',
        f'chat_botKeyboardButtonBackground={primary_txt}',
        f'chat_botKeyboardButtonBackgroundPressed={secondary_txt}',
        f'chat_botKeyboardButtonText={bg}',
        f'chat_botProgress={primary_txt}',
        f'chat_botSwitchToInlineText={secondary_txt}',
        f'chat_editDoneIcon={primary_txt}',
        f'chat_emojiPanelBackground={bg}',
        f'chat_emojiPanelBackspace={primary_txt}',
        f'chat_emojiPanelBadgeBackground={primary_txt}',
        f'chat_emojiPanelBadgeText={bg}',
        f'chat_emojiPanelEmptyText={primary_txt}',
        f'chat_emojiPanelIcon={secondary_txt}',
        f'chat_emojiPanelIconSelected={primary_txt}',
        f'chat_emojiPanelIconSelector={primary_txt}',
        f'chat_emojiPanelMasksIcon={secondary_txt}',
        f'chat_emojiPanelMasksIconSelected={secondary_txt}',
        'chat_emojiPanelNewTrending=13412811',
        f'chat_emojiPanelShadowLine={bg}',
        'chat_emojiPanelStickerPackSelector=1688849606',
        f'chat_emojiPanelStickerSetName={secondary_txt}',
        f'chat_emojiPanelStickerSetNameIcon={primary_txt}',
        f'chat_emojiPanelTrendingDescription={primary_txt}',
        f'chat_emojiPanelTrendingTitle={primary_txt}',
        f'chat_emojiSearchBackground={primary_txt}',
        f'chat_fieldOverlayText={primary_txt}',
        f'chat_goDownButton={bg}',
        f'chat_goDownButtonCounter={primary_txt}',
        f'chat_goDownButtonCounterBackground={bg}',
        f'chat_goDownButtonIcon={primary_txt}',
        f'chat_goDownButtonShadow={primary_txt}',
        f'chat_inAudioDurationSelectedText={primary_txt}',
        f'chat_inAudioDurationText={primary_txt}',
        f'chat_inAudioPerfomerSelectedText={primary_txt}',
        f'chat_inAudioPerfomerText={primary_txt}',
        f'chat_inAudioPerformerSelectedText={primary_txt}',
        f'chat_inAudioProgress={bg}',
        f'chat_inAudioSeekbar={secondary_txt}',
        f'chat_inAudioSeekbarFill={primary_txt}',
        f'chat_inAudioSeekbarSelected={secondary_txt}',
        f'chat_inAudioSelectedProgress={bg}',
        f'chat_inAudioTitleText={primary_txt}',
        f'chat_inBubble={chat_in_bubble}',
        'chat_inBubbleSelected=-514284193',
        f'chat_inBubbleShadow={secondary_txt}',
        f'chat_inContactBackground={primary_txt}',
        f'chat_inContactIcon={bg}',
        f'chat_inContactNameText={primary_txt}',
        f'chat_inContactPhoneText={primary_txt}',
        f'chat_inFileBackground={bg}',
        f'chat_inFileBackgroundSelected={bg}',
        f'chat_inFileIcon={primary_txt}',
        f'chat_inFileInfoSelectedText={primary_txt}',
        f'chat_inFileInfoText={primary_txt}',
        f'chat_inFileNameText={primary_txt}',
        f'chat_inFileProgress={bg}',
        f'chat_inFileProgressSelected={bg}',
        f'chat_inFileSelectedIcon={primary_txt}',
        f'chat_inForwardedNameText={primary_txt}',
        f'chat_inInstant={primary_txt}',
        f'chat_inInstantSelected={primary_txt}',
        f'chat_inlineResultIcon={primary_txt}',
        f'chat_inLoader={primary_txt}',
        f'chat_inLoaderPhoto={bg}',
        f'chat_inLoaderPhotoIcon={primary_txt}',
        f'chat_inLoaderPhotoIconSelected={primary_txt}',
        f'chat_inLoaderPhotoSelected={bg}',
        f'chat_inLoaderSelected={secondary_txt}',
        f'chat_inLocationBackground={bg}',
        f'chat_inLocationIcon={bg}',
        f'chat_inMenu={primary_txt}',
        f'chat_inMenuSelected={primary_txt}',
        f'chat_inPreviewInstantSelectedText={primary_txt}',
        f'chat_inPreviewInstantText={primary_txt}',
        f'chat_inPreviewLine={primary_txt}',
        f'chat_inReplyLine={primary_txt}',
        f'chat_inReplyMediaMessageSelectedText={primary_txt}',
        f'chat_inReplyMediaMessageText={primary_txt}',
        f'chat_inReplyMessageText={primary_txt}',
        f'chat_inReplyNameText={primary_txt}',
        f'chat_inSentClock={primary_txt}',
        f'chat_inSentClockSelected={primary_txt}',
        f'chat_inSiteNameText={primary_txt}',
        f'chat_inTimeSelectedText={primary_txt}',
        f'chat_inTimeText={primary_txt}',
        f'chat_inVenueInfoSelectedText={secondary_txt}',
        f'chat_inVenueInfoText={secondary_txt}',
        f'chat_inVenueNameText={secondary_txt}',
        f'chat_inViaBotNameText={primary_txt}',
        f'chat_inViews={primary_txt}',
        f'chat_inViewsSelected={primary_txt}',
        f'chat_inVoiceSeekbar={secondary_txt}',
        f'chat_inVoiceSeekbarFill={primary_txt}',
        f'chat_inVoiceSeekbarSelected={secondary_txt}',
        'chat_linkSelectBackground=852273611',
        f'chat_lockIcon={primary_txt}',
        f'chat_mediaLoaderPhotoIcon={primary_txt}',
        f'chat_mediaLoaderPhotoIconSelected={primary_txt}',
        'chat_mediaTimeText=-1',
        f'chat_messageLinkIn={secondary_txt}',
        f'chat_messageLinkOut={secondary_txt}',
        f'chat_messagePanelBackground={bg}',
        f'chat_messagePanelCancelInlineBot={primary_txt}',
        f'chat_messagePanelHint={secondary_txt}',
        f'chat_messagePanelIcons={primary_txt}',
        f'ChatShadow={primary_txt}',
        f'chat_messagePanelSend={secondary_txt}',
        f'chat_messagePanelShadow={bg}',
        f'chat_messagePanelText={primary_txt}',
        f'chat_messagePanelVoiceBackground={bg}',
        f'chat_messagePanelVoiceDelete={primary_txt}',
        f'chat_messagePanelVoiceDuration={primary_txt}',
        f'chat_messagePanelVoicePressed={primary_txt}',
        'chat_messagePanelVoiceShadow=265071051',
        f'chat_messageTextIn={primary_txt}',
        f'chat_messageTextOut={primary_txt}',
        f'chat_muteIcon={primary_txt}',
        f'chat_outAudioDurationSelectedText={primary_txt}',
        f'chat_outAudioDurationText={primary_txt}',
        f'chat_outAudioPerfomerText={primary_txt}',
        f'chat_outAudioPerformerSelectedText={primary_txt}',
        f'chat_outAudioProgress={bg}',
        f'chat_outAudioSeekbar={secondary_txt}',
        f'chat_outAudioSeekbarFill={primary_txt}',
        f'chat_outAudioSeekbarSelected={secondary_txt}',
        f'chat_outAudioSelectedProgress={bg}',
        f'chat_outAudioTitleText={primary_txt}',
        f'chat_outBubble={chat_out_bubble}',
        
        # f'chat_outBubbleGradient={secondary_txt}',
        # f'chat_outBubbleGradient2={chat_out_bubble}',
        # f'chat_outBubbleGradient3={secondary_txt}',
        
        f'chat_outBubbleSelected={chat_out_bubble}',
        f'chat_outBubbleShadow={secondary_txt}',
        f'chat_outContactBackground={primary_txt}',
        f'chat_outContactIcon={bg}',
        f'chat_outContactNameText={primary_txt}',
        f'chat_outContactPhoneText={primary_txt}',
        f'chat_outFileBackground={bg}',
        f'chat_outFileBackgroundSelected={bg}',
        f'chat_outFileIcon={primary_txt}',
        f'chat_outFileInfoSelectedText={primary_txt}',
        f'chat_outFileInfoText={primary_txt}',
        f'chat_outFileNameText={primary_txt}',
        f'chat_outFileProgress={bg}',
        f'chat_outFileProgressSelected={bg}',
        f'chat_outFileSelectedIcon={primary_txt}',
        f'chat_outForwardedNameText={primary_txt}',
        f'chat_outInstant={primary_txt}',
        f'chat_outInstantSelected={primary_txt}',
        f'chat_outLoader={primary_txt}',
        f'chat_outLoaderPhoto={bg}',
        f'chat_outLoaderPhotoIcon={primary_txt}',
        f'chat_outLoaderPhotoIconSelected={primary_txt}',
        f'chat_outLoaderPhotoSelected={bg}',
        f'chat_outLoaderSelected={secondary_txt}',
        f'chat_outLocationBackground={bg}',
        f'chat_outLocationIcon={bg}',
        f'chat_outMenu={primary_txt}',
        f'chat_outMenuSelected={primary_txt}',
        f'chat_outPreviewInstantSelectedText={primary_txt}',
        f'chat_outPreviewInstantText={primary_txt}',
        f'chat_outPreviewLine={primary_txt}',
        f'chat_outReplyLine={primary_txt}',
        f'chat_outReplyMediaMessageSelectedText={primary_txt}',
        f'chat_outReplyMediaMessageText={primary_txt}',
        f'chat_outReplyMessageText={primary_txt}',
        f'chat_outReplyNameText={primary_txt}',
        f'chat_outSentCheck={primary_txt}',
        f'chat_outSentCheckSelected={primary_txt}',
        f'chat_outSentClock={primary_txt}',
        f'chat_outSentClockSelected={primary_txt}',
        f'chat_outSiteNameText={primary_txt}',
        f'chat_outTimeSelectedText={primary_txt}',
        f'chat_outTimeText={primary_txt}',
        f'chat_outVenueInfoSelectedText={secondary_txt}',
        f'chat_outVenueInfoText={secondary_txt}',
        f'chat_outVenueNameText={secondary_txt}',
        f'chat_outViaBotNameText={primary_txt}',
        f'chat_outViews={primary_txt}',
        f'chat_outViewsSelected={primary_txt}',
        f'chat_outVoiceSeekbar={secondary_txt}',
        f'chat_outVoiceSeekbarFill={primary_txt}',
        f'chat_outVoiceSeekbarSelected={secondary_txt}',
        f'chat_previewDurationText={primary_txt}',
        f'chat_previewGameText={primary_txt}',
        f'chat_recordedVoiceBackground={bg}',
        f'chat_recordedVoiceDot={primary_txt}',
        f'chat_recordedVoicePlayPause={primary_txt}',
        f'chat_recordedVoicePlayPausePressed={secondary_txt}',
        f'chat_recordedVoiceProgress={secondary_txt}',
        f'chat_recordedVoiceProgressInner={primary_txt}',
        f'chat_recordTime={primary_txt}',
        f'chat_recordVoiceCancel={primary_txt}',
        f'chat_replyPanelClose={primary_txt}',
        f'chat_replyPanelIcons={primary_txt}',
        f'chat_replyPanelLine={primary_txt}',
        f'chat_replyPanelMessage={primary_txt}',
        f'chat_replyPanelName={primary_txt}',
        f'chat_reportSpam={primary_txt}',
        f'chat_searchPanelIcons={primary_txt}',
        f'chat_searchPanelText={primary_txt}',
        'chat_secretTimerBackground=-859002421',
        f'chat_secretTimerText={bg}',
        f'chat_secretTimeText={primary_txt}',
        'chat_selectedBackground=1691134411',
        f'chat_sentError={primary_txt}',
        f'chat_sentErrorIcon={bg}',
        f'chat_serviceBackground={ikb_bg}',
        f'chat_serviceBackgroundSelected={ikb_bg}',
        f'chat_serviceIcon={primary_txt}',
        f'chat_serviceLink={primary_txt}',
        f'chat_serviceText={primary_txt}',
        f'chat_stickerReplyLine={primary_txt}',
        f'chat_stickerReplyMessageText={primary_txt}',
        f'chat_stickerReplyNameText={primary_txt}',
        f'chat_stickersHintPanel={bg}',
        f'chat_stickerViaBotNameText={primary_txt}',
        'chat_textSelectBackground=1691134411',
        f'chat_topPanelBackground={bg}',
        f'chat_topPanelClose={primary_txt}',
        f'chat_topPanelLine={primary_txt}',
        f'chat_topPanelMessage={primary_txt}',
        f'chat_topPanelTitle={primary_txt}',
        f'chat_unreadMessagesStartArrowIcon={primary_txt}',
        f'chat_unreadMessagesStartBackground={bg}',
        f'chat_unreadMessagesStartText={primary_txt}',
        f'chats_actionBackground={primary_txt}',
        f'chats_actionIcon={bg}',
        f'chats_actionMessage={secondary_txt}',
        f'chats_actionPressedBackground={primary_txt}',
        f'chats_archiveBackground={primary_txt}',
        f'chats_archiveIcon={bg}',
        'chats_archivePinBackground=-926111285',
        f'chats_archiveText={bg}',
        f'chats_attachMessage={secondary_txt}',
        f'chats_date={primary_txt}',
        f'chats_draft={primary_txt}',
        f'chats_mentionIcon={bg}',
        f'chats_menuBackground={bg}',
        f'chats_menuCloud={primary_txt}',
        f'chats_menuCloudBackgroundCats={primary_txt}',
        f'chats_menuItemCheck={bg}',
        f'chats_menuItemIcon={primary_txt}',
        f'chats_menuItemText={primary_txt}',
        f'chats_menuName={primary_txt}',
        f'chats_menuPhone={primary_txt}',
        f'chats_menuPhoneCats={primary_txt}',
        f'chats_menuTopShadow={bg}',
        f'chats_message={secondary_txt}',
        'chats_message_threeLines=-65536',
        f'chats_muteIcon={primary_txt}',
        f'chats_name={primary_txt}',
        f'chats_nameArchived={primary_txt}',
        f'chats_nameIcon={primary_txt}',
        f'chats_nameMessage={primary_txt}',
        f'chats_nameMessage_threeLines={primary_txt}',
        f'chats_nameMessageArchived={primary_txt}',
        f'chats_nameMessageArchived_threeLines={primary_txt}',
        f'chats_pinnedIcon={primary_txt}',
        f'chats_pinnedOverlay={bg}',
        f'chats_secretIcon={primary_txt}',
        f'chats_secretName={primary_txt}',
        f'chats_sentCheck={primary_txt}',
        f'chats_sentClock={primary_txt}',
        f'chats_sentError={primary_txt}',
        f'chats_sentErrorIcon={bg}',
        f'chats_tabletSelectedOverlay={primary_txt}',
        f'chats_unreadCounter={primary_txt}',
        f'chats_unreadCounterMuted={secondary_txt}',
        f'chats_unreadCounterText={bg}',
        f'chats_verifiedBackground={primary_txt}',
        f'chats_verifiedCheck={bg}',
        f'checkbox={primary_txt}',
        f'checkboxCheck={bg}',
        f'checkboxSquareBackground={primary_txt}',
        f'checkboxSquareCheck={bg}',
        f'checkboxSquareDisabled={secondary_txt}',
        f'checkboxSquareUnchecked={primary_txt}',
        f'contacts_inviteBackground={bg}',
        f'contacts_inviteText={primary_txt}',
        f'contextProgressInner1={secondary_txt}',
        f'contextProgressOuter1={primary_txt}',
        f'dialogBackground={bg}',
        f'dialogBackgroundGray={bg}',
        f'dialogBadgeBackground={primary_txt}',
        f'dialogBadgeText={bg}',
        f'dialogButton={primary_txt}',
        'dialogButtonSelector=1691134411',
        f'dialogCheckboxSquareBackground={primary_txt}',
        f'dialogCheckboxSquareCheck={bg}',
        f'dialogCheckboxSquareDisabled={primary_txt}',
        f'dialogCheckboxSquareUnchecked={primary_txt}',
        'dialogFloatingButton=-1',
        f'dialogFloatingButtonPressed={bg}',
        f'dialogFloatingIcon={bg}',
        f'dialogGrayLine={primary_txt}',
        f'dialogIcon={primary_txt}',
        f'dialogInputField={primary_txt}',
        f'dialogInputFieldActivated={bg}',
        f'dialogLineProgress={primary_txt}',
        f'dialogLineProgressBackground={secondary_txt}',
        'dialogLinkSelection=852273611',
        f'dialogProgressCircle={primary_txt}',
        f'dialogRadioBackground={bg}',
        f'dialogRadioBackgroundChecked={primary_txt}',
        f'dialogRoundCheckBox={primary_txt}',
        f'dialogRoundCheckBoxCheck={bg}',
        f'dialogScrollGlow={primary_txt}',
        'dialogSearchBackground=1688849606',
        f'dialogSearchHint={secondary_txt}',
        f'dialogSearchIcon={secondary_txt}',
        f'dialogSearchText={primary_txt}',
        f'dialogShadowLine={secondary_txt}',
        f'dialogTextBlack={primary_txt}',
        f'dialogTextBlue2={primary_txt}',
        f'dialogTextBlue3={primary_txt}',
        f'dialogTextBlue4={primary_txt}',
        f'dialogTextBlue={primary_txt}',
        f'dialogTextGray2={primary_txt}',
        f'dialogTextGray={primary_txt}',
        f'dialogTextLink={primary_txt}',
        f'dialogTextRed={primary_txt}',
        'divider=13412811',
        f'emptyListPlaceholder={secondary_txt}',
        f'fastScrollActive={primary_txt}',
        f'fastScrollInactive={secondary_txt}',
        f'fastScrollText={bg}',
        f'featuredStickers_addButton={primary_txt}',
        f'featuredStickers_addButtonPressed={secondary_txt}',
        f'featuredStickers_addedIcon={primary_txt}',
        f'featuredStickers_buttonText={bg}',
        f'files_folderIcon={secondary_txt}',
        f'files_folderIconBackground={bg}',
        f'files_iconText={bg}',
        f'graySection={bg}',
        f'groupcreate_checkbox={primary_txt}',
        f'groupcreate_checkboxCheck={bg}',
        f'groupcreate_cursor={primary_txt}',
        f'groupcreate_hintText={primary_txt}',
        f'groupcreate_offlineText={primary_txt}',
        f'groupcreate_onlineText={primary_txt}',
        f'groupcreate_sectionShadow={bg}',
        f'groupcreate_sectionText={primary_txt}',
        f'groupcreate_spanBackground={primary_txt}',
        f'inappPlayerBackground={bg}',
        f'inappPlayerClose={primary_txt}',
        f'inappPlayerPerformer={primary_txt}',
        f'inappPlayerPlayPause={primary_txt}',
        f'inappPlayerTitle={primary_txt}',
        f'key_chat_messagePanelVoiceLock={primary_txt}',
        f'key_chat_messagePanelVoiceLockBackground={bg}',
        f'key_chat_messagePanelVoiceLockShadow={bg}',
        f'key_sheet_other={primary_txt}',
        f'key_sheet_scrollUp={primary_txt}',
        f'listSelectorSDK21={primary_txt}',
        f'location_liveLocationProgress={secondary_txt}',
        f'location_placeLocationBackground={secondary_txt}',
        f'location_sendLiveLocationBackground={secondary_txt}',
        f'location_sendLocationBackground={secondary_txt}',
        f'location_sendLocationIcon={bg}',
        f'musicPicker_buttonBackground={bg}',
        f'musicPicker_buttonIcon={secondary_txt}',
        f'musicPicker_checkbox={secondary_txt}',
        f'musicPicker_checkboxCheck={bg}',
        f'picker_badge={primary_txt}',
        f'picker_badgeText={bg}',
        f'picker_disabledButton={secondary_txt}',
        f'picker_enabledButton={primary_txt}',
        f'player_actionBar={bg}',
        f'player_actionBarItems={primary_txt}',
        f'player_actionBarSelector={primary_txt}',
        f'player_actionBarSubtitle={primary_txt}',
        f'player_actionBarTitle={primary_txt}',
        f'player_actionBarTop={bg}',
        f'player_background={bg}',
        f'player_button={primary_txt}',
        f'player_buttonActive={secondary_txt}',
        f'player_placeholder={primary_txt}',
        f'player_placeholderBackground={bg}',
        f'player_progress={primary_txt}',
        f'player_progressBackground={secondary_txt}',
        f'player_time={primary_txt}',
        f'profile_actionBackground={bg}',
        f'profile_actionIcon={primary_txt}',
        f'profile_actionPressedBackground={primary_txt}',
        f'profile_adminIcon={secondary_txt}',
        f'profile_creatorIcon={primary_txt}',
        f'profile_title={primary_txt}',
        f'profile_verifiedBackground={primary_txt}',
        f'profile_verifiedCheck={bg}',
        f'progressCircle={primary_txt}',
        f'radioBackground={primary_txt}',
        f'radioBackgroundChecked={primary_txt}',
        f'returnToCallBackground={bg}',
        f'returnToCallText={primary_txt}',
        f'sessions_devicesImage={secondary_txt}',
        f'sharedMedia_actionMode={bg}',
        f'sharedMedia_startStopLoadIcon={primary_txt}',
        f'stickers_menu={primary_txt}',
        f'stickers_menuSelector={primary_txt}',
        f'switch2Check={bg}',
        f'switch2Thumb={secondary_txt}',
        f'switch2ThumbChecked={secondary_txt}',
        'switch2Track=1269419206',
        f'switch2TrackChecked={secondary_txt}',
        'switchThumb=0',
        'switchThumbChecked=0',
        'switchTrack=1269419206',
        f'switchTrackChecked={secondary_txt}',
        f'undo_background={primary_txt}',
        f'undo_cancelColor={bg}',
        f'undo_infoColor={bg}',
        f'windowBackgroundGray={bg}',
        'windowBackgroundGrayShadow=0',
        f'windowBackgroundWhite={bg}',
        f'PreviewBackLinear={secondary_txt}',
        f'PreviewBackLinearShadow={bg}',
        f'windowBackgroundWhiteBlackText={primary_txt}',
        f'windowBackgroundWhiteBlueHeader={primary_txt}',
        f'windowBackgroundWhiteBlueText3={primary_txt}',
        f'windowBackgroundWhiteBlueText4={primary_txt}',
        f'windowBackgroundWhiteBlueText6={secondary_txt}',
        f'windowBackgroundWhiteBlueText7={secondary_txt}',
        f'windowBackgroundWhiteBlueText={primary_txt}',
        f'windowBackgroundWhiteGrayIcon={primary_txt}',
        f'windowBackgroundWhiteGrayText2={primary_txt}',
        f'windowBackgroundWhiteGrayText3={primary_txt}',
        f'windowBackgroundWhiteGrayText4={primary_txt}',
        f'windowBackgroundWhiteGrayText8={primary_txt}',
        f'windowBackgroundWhiteGrayText={primary_txt}',
        f'windowBackgroundWhiteGreenText2={primary_txt}',
        'windowBackgroundWhiteLinkSelection=849988806',
        f'windowBackgroundWhiteLinkText={secondary_txt}',
        f'windowBackgroundWhiteRedText2={primary_txt}',
        f'windowBackgroundWhiteRedText3={primary_txt}',
        f'windowBackgroundWhiteRedText4={primary_txt}',
        f'windowBackgroundWhiteRedText5={primary_txt}',
        f'windowBackgroundWhiteRedText6={primary_txt}',
        f'windowBackgroundWhiteRedText={primary_txt}',
        f'windowBackgroundWhiteValueText={secondary_txt}',
        f'PreviewBack={secondary_txt}',
        f'stories_circle_dialog1={bg}',
        f'stories_circle_dialog2={secondary_txt}',
        f'stories_circle_closeFriends1={bg}',
        f'stories_circle_closeFriends2={secondary_txt}',
        f'stories_circle1={bg}',
        f'stories_circle2={secondary_txt}',
    ]

    user_directory = os.path.join('android', 'theme', str(chat_id))
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)

    theme = os.path.join('android', 'theme', str(chat_id), file_name)

    with open(theme, 'wb') as f:
        for row in data:
            f.write(f'{row}\n'.encode('utf-8'))
        f.write('\nWPS\n'.encode('utf-8'))
        f.write(binar_imag)
        f.write('\nWPE'.encode('utf-8'))

    return theme