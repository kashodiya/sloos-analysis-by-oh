#!/usr/bin/env python3
"""
Screenshot script for SLOOS application using Playwright
"""
import asyncio
import os
from playwright.async_api import async_playwright

# Configuration
APP_URL = "http://localhost:7251"
SCREENSHOT_DIR = "screenshots"
WAIT_TIME = 6000  # milliseconds

async def take_screenshots():
    """Take screenshots of all pages in the SLOOS application"""
    
    # Create screenshots directory
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    
    async with async_playwright() as p:
        print("🚀 Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            # Screenshot 1: Executive Dashboard (default page)
            print(f"📱 Navigating to {APP_URL}...")
            await page.goto(APP_URL, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(WAIT_TIME)
            print("📸 Taking screenshot 1: Executive Dashboard...")
            await page.screenshot(path=f"{SCREENSHOT_DIR}/01_executive_dashboard.png", full_page=True)
            
            # Screenshot 2: Data Explorer - use direct URL
            print("📸 Taking screenshot 2: Data Explorer...")
            await page.goto(f"{APP_URL}/?page=Data_Explorer", wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(WAIT_TIME)
            await page.screenshot(path=f"{SCREENSHOT_DIR}/02_data_explorer.png", full_page=True)
            
            # Screenshot 3: Data Explorer scrolled
            print("📸 Taking screenshot 3: Data Explorer scrolled...")
            await page.evaluate("window.scrollTo(0, 600)")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"{SCREENSHOT_DIR}/03_data_explorer_scrolled.png", full_page=False)
            
            # Screenshot 4: AI Analysis
            print("📸 Taking screenshot 4: AI Analysis...")
            await page.goto(f"{APP_URL}/?page=AI_Analysis", wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(WAIT_TIME)
            await page.screenshot(path=f"{SCREENSHOT_DIR}/04_ai_analysis.png", full_page=True)
            
            # Screenshot 5: Data Management
            print("📸 Taking screenshot 5: Data Management...")
            await page.goto(f"{APP_URL}/?page=Data_Management", wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(WAIT_TIME)
            await page.screenshot(path=f"{SCREENSHOT_DIR}/05_data_management.png", full_page=True)
            
            # Screenshot 6: Back to Dashboard for final shot
            print("📸 Taking screenshot 6: Dashboard detail view...")
            await page.goto(APP_URL, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(WAIT_TIME)
            await page.evaluate("window.scrollTo(0, 400)")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=f"{SCREENSHOT_DIR}/06_dashboard_scrolled.png", full_page=False)
            
            print("✅ All screenshots captured successfully!")
            print(f"📁 Screenshots saved to: {os.path.abspath(SCREENSHOT_DIR)}/")
            
        except Exception as e:
            print(f"❌ Error taking screenshots: {e}")
            raise
        finally:
            await browser.close()

async def main():
    """Main function"""
    print("=" * 80)
    print("📸 SLOOS Application Screenshot Tool")
    print("=" * 80)
    print()
    
    await take_screenshots()
    
    print()
    print("=" * 80)
    print("✅ Screenshot capture complete!")
    print("=" * 80)
    print()
    print("Screenshots:")
    for i, name in enumerate([
        "01_executive_dashboard.png - Main dashboard with metrics",
        "02_data_explorer.png - Data explorer page",
        "03_data_explorer_scrolled.png - Data explorer detail view",
        "04_ai_analysis.png - AI-powered analysis page",
        "05_data_management.png - Data management page",
        "06_dashboard_scrolled.png - Dashboard detail view"
    ], 1):
        print(f"  {i}. {name}")

if __name__ == "__main__":
    asyncio.run(main())
