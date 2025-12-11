#!/usr/bin/env python3
"""
Complete Setup Script for Tour Operator Website

This script provides a one-command setup for the entire tour operator system.
It handles migrations and sample data loading automatically.

Usage: python3 setup.py
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Tour Operator Complete Setup")
    print("=" * 50)
    print()

    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the tour_operator directory.")
        sys.exit(1)

    # Step 1: Remove existing database for fresh start
    if os.path.exists('db.sqlite3'):
        print("🗑️ Removing existing database for fresh start...")
        os.remove('db.sqlite3')
        print("✅ Database removed")

    # Step 2: Run migrations
    if not run_command('python3 manage.py migrate', 'Running Django migrations'):
        sys.exit(1)

    # Step 3: Load sample data
    if not run_command('python3 load.py', 'Loading sample data with images'):
        sys.exit(1)

    print()
    print("=" * 50)
    print("🎉 SETUP COMPLETE!")
    print("=" * 50)
    print()
    print("🔑 LOGIN CREDENTIALS:")
    print("------------------------")
    print("👤 Customer: john_customer / customer123")
    print("🧭 Guide: sarah_guide / guide123")
    print("🔧 Admin: admin / admin123 (hardcoded)")
    print()
    print("🌐 TO START THE SERVER:")
    print("------------------------")
    print("python3 manage.py runserver")
    print()
    print("🏠 Then visit: http://127.0.0.1:8000")
    print()
    print("✨ Your tour operator website is ready with:")
    print("   • 3 tours with beautiful image galleries")
    print("   • Complete user accounts (customer & guide)")
    print("   • Sample bookings and feedback")
    print("   • Full admin and guide dashboards")

if __name__ == '__main__':
    main()