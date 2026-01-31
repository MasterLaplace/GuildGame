// Fill out your copyright notice in the Description page of Project Settings.


#include "CursorInteractComponent.h"
#include "../Player/GuildPlayerController.h"
#include "Engine/World.h"

// Sets default values for this component's properties
UCursorInteractComponent::UCursorInteractComponent()
{
    // Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
    // off to improve performance if you don't need them.
    PrimaryComponentTick.bCanEverTick = false;
}


// Called when the game starts
void UCursorInteractComponent::BeginPlay()
{
    Super::BeginPlay();

    if (AActor *onwer = GetOwner(); onwer)
    {
        onwer->OnBeginCursorOver.AddDynamic(this, &UCursorInteractComponent::OnBeginCursorOver);
        onwer->OnEndCursorOver.AddDynamic(this, &UCursorInteractComponent::OnEndCursorOver);
    }
}

void UCursorInteractComponent::OnBeginCursorOver(AActor *touchedActor)
{
    if (AGuildPlayerController *pc = Cast<AGuildPlayerController>(GetWorld()->GetFirstPlayerController()); pc)
    {
        pc->SetCursorToInteract(true);
    }
}

void UCursorInteractComponent::OnEndCursorOver(AActor *touchedActor)
{
    if (AGuildPlayerController *pc = Cast<AGuildPlayerController>(GetWorld()->GetFirstPlayerController()); pc)
    {
        pc->SetCursorToInteract(false);
    }
}


// Called every frame
void UCursorInteractComponent::TickComponent(float deltaTime, ELevelTick tickType, FActorComponentTickFunction *thisTickFunction)
{
    Super::TickComponent(deltaTime, tickType, thisTickFunction);
}
