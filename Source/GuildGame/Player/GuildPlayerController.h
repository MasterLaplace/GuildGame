// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "GuildPlayerController.generated.h"

/**
 *
 */
UCLASS()
class GUILDGAME_API AGuildPlayerController : public APlayerController
{
    GENERATED_BODY()

public:
    AGuildPlayerController();

    virtual void BeginPlay() override;

    UFUNCTION(BlueprintCallable, Category = "Cursor")
    void SetCursorToInteract(bool isHovering);

private:
    void SetHardwareCursorFromTexture(EMouseCursor::Type cursorType, UTexture2D *cursorTexture, FVector2D hotSpot);

protected:
    UPROPERTY(EditDefaultsOnly, Category = "Cursor")
    FName _cursorIdlePath = TEXT("/Game/Art/UI/Cursors/CursorIdle");

    UPROPERTY(EditDefaultsOnly, Category = "Cursor")
    FName _cursorInteractPath = TEXT("/Game/Art/UI/Cursors/CursorInteract");

private:
    UTexture2D *_cursorIdle;
    UTexture2D *_cursorInteract;
};
