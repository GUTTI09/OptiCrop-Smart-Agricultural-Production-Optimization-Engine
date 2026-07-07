"""
CropModel: rule-based crop recommendation engine for OptiCrop.

This class encapsulates the crop-recommendation logic (previously implemented
client-side in JavaScript) so it can run server-side and be persisted as
model.pkl, exactly like a trained ML model would be loaded in app.py.
"""


class CropModel:
    """A simple rule-based recommender keyed on temperature, humidity,
    rainfall, soil pH, and N-P-K nutrient levels."""

    def predict(self, temp, humidity, rainfall, ph, n, p, k):
        crop = {}
    
    

        # 1. RICE - High water, warm, acidic to neutral
        if 20 <= temp <= 35 and rainfall >= 150 and 5.5 <= ph <= 7.0 and humidity >= 60:
            crop = {
                'name': 'Rice (Paddy)',
                'icon': 'fa-seedling',
                'yield': '6-10 tons/hectare',
                'season': '4-6 months',
                'water': 'Very High (flooded conditions)',
                'sunlight': '6-8 hours daily',
                'confidence': 94,
                'tips': [
                    'Maintain 5-10cm standing water during vegetative stage',
                    'Apply nitrogen in 3 split doses (basal, tillering, panicle)',
                    'Use phosphorus for root development',
                    'Monitor for blast, sheath blight, and stem borer',
                    'Drain field 1-2 weeks before harvest'
                ]
            }
        # 2. WHEAT - Cool, moderate water, neutral pH
        elif 12 <= temp <= 25 and 40 <= rainfall <= 80 and 6.0 <= ph <= 7.5 and humidity >= 40:
            crop = {
                'name': 'Wheat',
                'icon': 'fa-wheat-awn',
                'yield': '4-7 tons/hectare',
                'season': '3-4 months',
                'water': 'Moderate (5-6 irrigations)',
                'sunlight': '5-7 hours daily',
                'confidence': 91,
                'tips': [
                    'Sow in well-prepared, firm seedbed',
                    'Apply 120-150 kg N/ha in 3 splits',
                    'Critical irrigation at crown root, tillering, flowering stages',
                    'Watch for rust diseases and aphids',
                    'Harvest when grain moisture is 12-14%'
                ]
            }
        # 3. MAIZE/CORN - Warm, moderate water
        elif 18 <= temp <= 30 and 60 <= rainfall <= 120 and 5.5 <= ph <= 7.0 and n >= 80:
            crop = {
                'name': 'Maize (Corn)',
                'icon': 'fa-leaf',
                'yield': '8-12 tons/hectare',
                'season': '3-4 months',
                'water': 'Moderate to High',
                'sunlight': '7-9 hours daily',
                'confidence': 89,
                'tips': [
                    'Plant in rows 60-75cm apart',
                    'High nitrogen requirement (150-200 kg/ha)',
                    'Hill up soil at knee-height stage',
                    'Critical water at tasseling and silking',
                    'Harvest when black layer forms at kernel base'
                ]
            }
        # 4. SOYBEAN - Warm, moderate rainfall, good drainage
        elif 20 <= temp <= 30 and 70 <= rainfall <= 120 and 6.0 <= ph <= 7.0 and p >= 30:
            crop = {
                'name': 'Soybean',
                'icon': 'fa-seedling',
                'yield': '2.5-4 tons/hectare',
                'season': '3-4 months',
                'water': 'Moderate (avoid waterlogging)',
                'sunlight': '6-8 hours daily',
                'confidence': 87,
                'tips': [
                    'Inoculate seeds with rhizobium culture',
                    'Apply phosphorus at planting (60-80 kg/ha)',
                    'Critical irrigation at flowering and pod filling',
                    'Monitor for defoliators and pod borer',
                    'Harvest when 95% pods turn brown'
                ]
            }
        # 5. COTTON - Hot, low humidity, long season
        elif 25 <= temp <= 35 and 50 <= rainfall <= 80 and 6.0 <= ph <= 8.0 and humidity <= 60:
            crop = {
                'name': 'Cotton',
                'icon': 'fa-cloud',
                'yield': '1.5-3 tons/hectare (lint)',
                'season': '5-7 months',
                'water': 'Moderate (drought tolerant)',
                'sunlight': '8-10 hours daily',
                'confidence': 85,
                'tips': [
                    'Requires long frost-free period',
                    'High potassium requirement for boll development',
                    'Control bollworm, whitefly, and aphids',
                    'Pick cotton when bolls fully open',
                    'Rotate with non-malvaceous crops'
                ]
            }
        # 6. SUGARCANE - Hot, high water, long duration
        elif 20 <= temp <= 35 and rainfall >= 120 and 6.0 <= ph <= 7.5 and k >= 100:
            crop = {
                'name': 'Sugarcane',
                'icon': 'fa-candy-cane',
                'yield': '80-120 tons/hectare',
                'season': '10-18 months',
                'water': 'Very High (regular irrigation)',
                'sunlight': '8-10 hours daily',
                'confidence': 92,
                'tips': [
                    'High potassium requirement (150-200 kg/ha)',
                    'Apply nitrogen in splits over 6 months',
                    'Earthing up at 4 and 6 months',
                    'Control red rot, smut, and borers',
                    'Harvest at 10-12% sugar content'
                ]
            }
        # 7. POTATO - Cool, moderate water, acidic soil
        elif 15 <= temp <= 25 and 50 <= rainfall <= 80 and 5.0 <= ph <= 6.5 and k >= 80:
            crop = {
                'name': 'Potato',
                'icon': 'fa-apple-alt',
                'yield': '25-40 tons/hectare',
                'season': '3-4 months',
                'water': 'Moderate (consistent moisture)',
                'sunlight': '6-8 hours daily',
                'confidence': 88,
                'tips': [
                    'High potassium for tuber development',
                    'Hill soil around plants twice',
                    'Avoid water stress during tuberization',
                    'Control late blight and aphids',
                    'Harvest when vines dry down'
                ]
            }
        # 8. TOMATO - Warm, moderate water, slightly acidic
        elif 18 <= temp <= 28 and 60 <= rainfall <= 100 and 6.0 <= ph <= 6.8 and n >= 100:
            crop = {
                'name': 'Tomato',
                'icon': 'fa-apple-alt',
                'yield': '40-60 tons/hectare',
                'season': '3-4 months',
                'water': 'Moderate (drip irrigation best)',
                'sunlight': '7-9 hours daily',
                'confidence': 86,
                'tips': [
                    'High nitrogen for vegetative growth',
                    'Stake or cage for support',
                    'Calcium to prevent blossom end rot',
                    'Control whitefly, fruit borer, blight',
                    'Harvest at breaker stage for transport'
                ]
            }
        # 9. ONION - Cool to moderate, low-moderate water
        elif 12 <= temp <= 25 and 40 <= rainfall <= 70 and 6.0 <= ph <= 7.0 and p >= 40:
            crop = {
                'name': 'Onion',
                'icon': 'fa-layer-group',
                'yield': '20-30 tons/hectare',
                'season': '4-5 months',
                'water': 'Low to Moderate',
                'sunlight': '6-8 hours daily',
                'confidence': 84,
                'tips': [
                    'Phosphorus critical for bulb development',
                    'Reduce irrigation before harvest',
                    'Cure bulbs in shade for 2-3 weeks',
                    'Control thrips and purple blotch',
                    'Store in well-ventilated area'
                ]
            }
        # 10. BARLEY - Cool, drought tolerant
        elif 10 <= temp <= 22 and 30 <= rainfall <= 60 and 6.0 <= ph <= 8.0:
            crop = {
                'name': 'Barley',
                'icon': 'fa-wheat-awn',
                'yield': '3-5 tons/hectare',
                'season': '3-4 months',
                'water': 'Low (drought tolerant)',
                'sunlight': '6-8 hours daily',
                'confidence': 82,
                'tips': [
                    'More salt and drought tolerant than wheat',
                    'Apply 80-100 kg N/ha',
                    'Good for marginal soils',
                    'Watch for leaf stripe and aphids',
                    'Harvest when moisture is 12-13%'
                ]
            }
        # 11. MILLET (Pearl/Bajra) - Hot, dry, low rainfall
        elif 25 <= temp <= 35 and 40 <= rainfall <= 80 and 6.0 <= ph <= 8.0 and humidity <= 60:
            crop = {
                'name': 'Pearl Millet (Bajra)',
                'icon': 'fa-seedling',
                'yield': '2-4 tons/hectare',
                'season': '2-3 months',
                'water': 'Low (very drought tolerant)',
                'sunlight': '8-10 hours daily',
                'confidence': 83,
                'tips': [
                    'Excellent for dryland farming',
                    'Apply 60-80 kg N/ha',
                    'Downy mildew resistant varieties preferred',
                    'Harvest when grains harden',
                    'Good for rotational cropping'
                ]
            }
        # 12. GROUNDNUT/PEANUT - Warm, sandy soil, moderate water
        elif 20 <= temp <= 30 and 60 <= rainfall <= 100 and 5.5 <= ph <= 7.0 and p >= 30 and k >= 40:
            crop = {
                'name': 'Groundnut (Peanut)',
                'icon': 'fa-nut',
                'yield': '2-3.5 tons/hectare',
                'season': '4-5 months',
                'water': 'Moderate (critical at flowering)',
                'sunlight': '7-9 hours daily',
                'confidence': 86,
                'tips': [
                    'Light, sandy loam soil ideal',
                    'Gypsum application at flowering',
                    'Phosphorus for root and peg development',
                    'Control leaf spot and aphids',
                    'Harvest when 70% pods mature'
                ]
            }
        # 13. SUNFLOWER - Warm, moderate water
        elif 18 <= temp <= 28 and 50 <= rainfall <= 90 and 6.0 <= ph <= 7.5:
            crop = {
                'name': 'Sunflower',
                'icon': 'fa-sun',
                'yield': '1.5-2.5 tons/hectare',
                'season': '3-4 months',
                'water': 'Moderate',
                'sunlight': '8-10 hours daily',
                'confidence': 84,
                'tips': [
                    'High oil content crop',
                    'Apply 80-100 kg N/ha',
                    'Boron application increases yield',
                    'Control capitulum borer and rust',
                    'Harvest when back of head turns yellow'
                ]
            }
        # 14. MUSTARD/RAPESEED - Cool, moderate water
        elif 10 <= temp <= 25 and 40 <= rainfall <= 70 and 6.0 <= ph <= 7.5 and n >= 60:
            crop = {
                'name': 'Mustard (Rapeseed)',
                'icon': 'fa-seedling',
                'yield': '1.5-2.5 tons/hectare',
                'season': '3-4 months',
                'water': 'Moderate',
                'sunlight': '6-8 hours daily',
                'confidence': 85,
                'tips': [
                    'Important oilseed crop',
                    'Apply nitrogen in 2 splits',
                    'Sulfur application increases oil content',
                    'Control aphids and white rust',
                    'Harvest when pods turn yellowish-brown'
                ]
            }
        # 15. CHICKPEA (GRAM) - Cool, low water
        elif 15 <= temp <= 25 and 30 <= rainfall <= 60 and 6.0 <= ph <= 7.5 and p >= 30:
            crop = {
                'name': 'Chickpea (Gram)',
                'icon': 'fa-seedling',
                'yield': '1.5-2.5 tons/hectare',
                'season': '3-4 months',
                'water': 'Low (drought tolerant)',
                'sunlight': '6-8 hours daily',
                'confidence': 83,
                'tips': [
                    'Cool season legume',
                    'Inoculate with rhizobium',
                    'Phosphorus essential for nodulation',
                    'Control pod borer and wilt',
                    'Harvest when plants dry and pods rattle'
                ]
            }
        # 16. LENTIL - Cool, low-moderate water
        elif 10 <= temp <= 22 and 35 <= rainfall <= 65 and 6.0 <= ph <= 7.0:
            crop = {
                'name': 'Lentil (Masoor)',
                'icon': 'fa-seedling',
                'yield': '1-1.8 tons/hectare',
                'season': '3-4 months',
                'water': 'Low to Moderate',
                'sunlight': '6-8 hours daily',
                'confidence': 81,
                'tips': [
                    'Short duration rabi crop',
                    'Inoculate seeds with rhizobium',
                    'Apply phosphorus at sowing',
                    'Control stemphylium blight and aphids',
                    'Harvest when 80% pods mature'
                ]
            }
        # 17. COFFEE - Warm, high rainfall, acidic
        elif 15 <= temp <= 25 and 150 <= rainfall <= 250 and 5.0 <= ph <= 6.5 and humidity >= 70:
            crop = {
                'name': 'Coffee (Arabica/Robusta)',
                'icon': 'fa-coffee',
                'yield': '1-2 tons/hectare (beans)',
                'season': 'Perennial (3-4 years to mature)',
                'water': 'High (well-distributed)',
                'sunlight': 'Filtered light (shade grown)',
                'confidence': 90,
                'tips': [
                    'Requires 1500-2500mm annual rainfall',
                    'Acidic, well-drained soil essential',
                    'Regular pruning for productivity',
                    'Control berry borer and leaf rust',
                    'Harvest when cherries turn red'
                ]
            }
        # 18. TEA - Warm, very high rainfall, acidic
        elif 15 <= temp <= 28 and 150 <= rainfall <= 300 and 4.5 <= ph <= 5.5 and humidity >= 70:
            crop = {
                'name': 'Tea',
                'icon': 'fa-mug-hot',
                'yield': '1.5-3 tons/hectare (made tea)',
                'season': 'Perennial (3 years to mature)',
                'water': 'Very High (2000mm+ annually)',
                'sunlight': 'Partial shade beneficial',
                'confidence': 91,
                'tips': [
                    'Acidic soil (pH 4.5-5.5) essential',
                    'High nitrogen requirement',
                    'Regular pruning and plucking',
                    'Control mosquito bug and blister blight',
                    'Pluck two leaves and a bud'
                ]
            }
        # 19. BANANA - Hot, very high water
        elif 20 <= temp <= 32 and rainfall >= 150 and 5.5 <= ph <= 7.0 and k >= 120:
            crop = {
                'name': 'Banana',
                'icon': 'fa-pepper-hot',
                'yield': '40-80 tons/hectare',
                'season': '12-15 months',
                'water': 'Very High (daily irrigation)',
                'sunlight': '8-10 hours daily',
                'confidence': 89,
                'tips': [
                    'Very high potassium requirement',
                    'Drip irrigation most efficient',
                    'Propping to prevent toppling',
                    'Control Panama wilt and sigatoka',
                    'Harvest when fruits are 3/4 mature'
                ]
            }
        # 20. MANGO - Hot, moderate water
        elif 20 <= temp <= 35 and 70 <= rainfall <= 150 and 5.5 <= ph <= 7.5:
            crop = {
                'name': 'Mango',
                'icon': 'fa-apple-alt',
                'yield': '10-20 tons/hectare',
                'season': 'Perennial (5-6 years to mature)',
                'water': 'Moderate (critical at flowering)',
                'sunlight': 'Full sun (8-10 hours)',
                'confidence': 87,
                'tips': [
                    'Deep, well-drained soil preferred',
                    'Irrigate during flowering and fruit set',
                    'Prune for shape and size control',
                    'Control fruit fly and powdery mildew',
                    'Harvest at mature green stage'
                ]
            }
        # 21. PAPAYA - Warm, moderate-high water
        elif 18 <= temp <= 30 and 100 <= rainfall <= 200 and 5.5 <= ph <= 7.0:
            crop = {
                'name': 'Papaya',
                'icon': 'fa-apple-alt',
                'yield': '60-100 tons/hectare',
                'season': '9-12 months',
                'water': 'Moderate to High',
                'sunlight': 'Full sun',
                'confidence': 85,
                'tips': [
                    'Fast-growing fruit crop',
                    'Requires good drainage',
                    'Regular fertigation',
                    'Control ringspot virus and mites',
                    'Harvest when 1/4 surface yellow'
                ]
            }
        # DEFAULT - Mixed Vegetables / general recommendation
        else:
            crop = {
                'name': 'Mixed Vegetables',
                'icon': 'fa-carrot',
                'yield': '15-25 tons/hectare',
                'season': '2-4 months',
                'water': 'Moderate',
                'sunlight': '5-7 hours daily',
                'confidence': 78,
                'tips': [
                    'Use organic compost regularly',
                    'Practice crop rotation',
                    'Implement drip irrigation',
                    'Use natural pest control methods',
                    'Consider greenhouse cultivation'
                ]
            }

        return crop
