# Duolingo Observer - A Home Assistant integration for Duolingo

_Home Assistant integration to track users Duolingo progress._

## About


This integration is easy to set up, just enter your username. Once configured, it automatically creates sensors that track user's Duolingo streak, overall progress, and progress per individual course.

- **🔥 Binary Streak Today Sensor**: Shows if the user’s streak was extended today (on/off).
- **📅 Streak Length Sensor**: Displays user’s current streak count in days
- **⭐ Total XP Sensor**: Shows user’s total XP across all courses
- **⭐ Course XP Sensor**: Shows user’s XP by language course


⚠️ **Important**: This integration uses reverse-engineered Duolingo APIs since no official API documentation exists. It may break if Duolingo changes their endpoints.

## Installation

### Manual Installation

1. Download the latest release or clone this repository
2. Copy the `custom_components/duolingo/` folder to your Home Assistant `custom_components/` directory
3. Restart Home Assistant
4. Go to **Settings → Devices & Services → Add Integration** and search for "Duolingo Observer"

### HACS Installation

Add this repository as a custom repository in HACS:

1. Go to HACS → Integrations → ⋮ → Custom repositories
2. Add repository URL: `https://github.com/EvGeniyLell/Duolingo-HAi`
3. Category: Integration
4. Install and restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for "Duolingo Observer"
3. Enter user’s Duolingo username (the one visible in profile URL)
4. The integration will create a few entities for tracking user’s streak
