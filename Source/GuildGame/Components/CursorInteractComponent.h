// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "CursorInteractComponent.generated.h"


UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class GUILDGAME_API UCursorInteractComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    // Sets default values for this component's properties
    UCursorInteractComponent();

protected:
    // Called when the game starts
    virtual void BeginPlay() override;

    UFUNCTION()
    void OnBeginCursorOver(AActor *touchedActor);

    UFUNCTION()
    void OnEndCursorOver(AActor *touchedActor);

public:
    // Called every frame
    virtual void TickComponent(float deltaTime, ELevelTick tickType, FActorComponentTickFunction *thisTickFunction) override;
};
