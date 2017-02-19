var mongoose = require('mongoose');

var Animals = mongoose.model('Animal', {
     animalID : Number,
     animalOrgID : Number,
     animalActivityLevel : String,
     animalAdoptedDate : Date,
     animalAdoptionFee : Number,
     animalAgeString : String,
     animalAltered :  Boolean,
     animalAvailableDate : Date,
     animalBirthdate : Date,
     animalBirthdateExact : Boolean,
     animalBreed : String,
     animalCoatLength : Number,
     animalColor : String,
     animalColorID : Number,
     animalColorDetails : String,
     animalCourtesy : Boolean,
     animalDeclawed :  Boolean,
     animalDescription : String,
     animalDescriptionPlain : String,
     animalDistinguishingMarks : String,
     animalEarType : String,
     animalEnergyLevel : String,
     animalExerciseNeeds : String,
     animalEyeColor : String,
     animalFence : String,
     animalFound : Boolean,
     animalFoundDate : Date,
     animalFoundPostalcode : Number,
     animalGeneralAge : String,
     animalGeneralSizePotential : String,
     animalGroomingNeeds : String,
     animalHousetrained : Boolean,
     animalIndoorOutdoor : String,
     animalKillDate : Date,
     animalKillReason : String,
     animalLocation :  Number,
     animalLocationCoordinates :  String,
     animalLocationDistance : Number,
     animalLocationCitystate :  String,
     animalMicrochipped : Boolean,
     animalMixedBreed : Boolean,
     animalName :  String,
     animalSpecialneeds : Boolean,
     animalSpecialneedsDescription : String,
     animalNeedsFoster : Boolean,
     animalNewPeople : String,
     animalNotHousetrainedReason : String,
     animalObedienceTraining : Boolean,
     animalOKWithAdults : Boolean,
     animalOKWithCats : Boolean,
     animalOKWithDogs : Boolean,
     animalOKWithKids : Boolean,
     animalOwnerExperience : String,
     animalPattern : String,
     animalPatternID : Number,
     animalAdoptionPending : Boolean,
     animalPrimaryBreed : String,
     animalPrimaryBreedID : Number,
     animalRescueID : String,
     animalSearchString :  String,
     animalSecondaryBreed : String,
     animalSecondaryBreedID :  Number,
     animalSex : String,
     animalShedding : Boolean,
     animalSizeCurrent :  Number,
     animalSizePotential : Number,
     animalSizeUOM : String,
     animalSpecies : String,
     animalSpeciesID : String,
     animalSponsorable : Boolean,
     animalSponsors : String,
     animalSponsorshipDetails : String,
     animalSponsorshipMinimum : String,
     animalStatus : String,
     animalStatusID : Number,
     animalSummary : String,
     animalTailType : String,
     animalThumbnailUrl : String,
     animalUptodate : Boolean,
     animalUpdatedDate : String,
     animalUrl : String,
     animalVocal : Boolean,
     animalYardRequired : Boolean,
     animalAffectionate : Boolean,
     animalApartment : Boolean,
     animalCratetrained : Boolean,
     animalDrools : Boolean,
     animalEagerToPlease : Boolean,
     animalEscapes : Boolean,
     animalEventempered : Boolean,
     animalFetches : Boolean,
     animalGentle : Boolean,
     animalGoodInCar : Boolean,
     animalGoofy : Boolean,
     animalHasAllergies : Boolean,
     animalHearingImpaired : Boolean,
     animalHypoallergenic : Boolean,
     animalIndependent : Boolean,
     animalIntelligent : Boolean,
     animalLap : Boolean,
     animalLeashtrained : Boolean,
     animalNeedsCompanionAnimal : Boolean,
     animalNoCold : Boolean,
     animalNoFemaleDogs : Boolean,
     animalNoHeat : Boolean,
     animalNoLargeDogs : Boolean,
     animalNoMaleDogs : Boolean,
     animalNoSmallDogs : Boolean,
     animalObedient : Boolean,
     animalOKForSeniors : Boolean,
     animalOKWithFarmAnimals : Boolean,
     animalOlderKidsOnly : Boolean,
     animalOngoingMedical : Boolean,
     animalPlayful : Boolean,
     animalPlaysToys : Boolean,
     animalPredatory : Boolean,
     animalProtective : Boolean,
     animalSightImpaired : Boolean,
     animalSkittish : Boolean,
     animalSpecialDiet : Boolean,
     animalSwims : Boolean,
     animalTimid : Boolean,
     fosterEmail : String,
     fosterFirstname : String,
     fosterLastname : String,
     fosterName : String,
     fosterPhoneCell : String,
     fosterPhoneHome : String,
     fosterSalutation : String,
     locationAddress : String,
     locationCity : String,
     locationCountry : String,
     locationUrl : String,
     locationName : String,
     locationPhone : String,
     locationState : String,
     locationPostalcode : String,
     animalPictures : Array,
     animalVideos : Array,
     animalVideoUrls : Array


})

module.exports = Animals;
