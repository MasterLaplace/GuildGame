// Fill out your copyright notice in the Description page of Project Settings.


#include "GuildPlayerController.h"
#include "Engine/Texture2D.h"
#include "Engine/Engine.h"
#include "Engine/LocalPlayer.h"
#include "Engine/GameViewportClient.h"

AGuildPlayerController::AGuildPlayerController()
{
    bShowMouseCursor = true;
}

void AGuildPlayerController::BeginPlay()
{
    Super::BeginPlay();

    _cursorIdle = Cast<UTexture2D>(StaticLoadObject(UTexture2D::StaticClass(), nullptr, *_cursorIdlePath.ToString()));
    _cursorInteract = Cast<UTexture2D>(StaticLoadObject(UTexture2D::StaticClass(), nullptr, *_cursorInteractPath.ToString()));

    if (_cursorIdle)
        SetHardwareCursorFromTexture(EMouseCursor::Default, _cursorIdle, FVector2D(32, 32));
}

void AGuildPlayerController::SetCursorToInteract(bool isHovering)
{
    if (UTexture2D *targetCursor = isHovering ? _cursorInteract : _cursorIdle; targetCursor)
    {
        SetHardwareCursorFromTexture(EMouseCursor::Default, targetCursor, FVector2D(32, 32));
    }
}

void AGuildPlayerController::SetHardwareCursorFromTexture(EMouseCursor::Type CursorType, UTexture2D* CursorTexture, FVector2D HotSpot)
{
    if (!CursorTexture)
        return;

    if (ULocalPlayer* LocalPlayer = Cast<ULocalPlayer>(Player))
    {
        if (UGameViewportClient* ViewportClient = LocalPlayer->ViewportClient)
        {
            ViewportClient->SetHardwareCursor(CursorType, FName(*CursorTexture->GetPathName()), HotSpot);
        }
    }
}
