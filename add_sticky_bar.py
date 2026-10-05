#!/usr/bin/env python3
"""
Script to add mobile sticky conversion bar to all HTML pages
"""

import os
import re

# CSS styles for sticky conversion bar
STICKY_BAR_CSS = '''
        /* ===== Mobile Sticky Conversion Bar ===== */
        .sticky-conversion-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #ffffff;
            padding: 12px 14px 16px;
            box-shadow: 0 -6px 30px rgba(0, 0, 0, 0.15);
            z-index: 999;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            border-top: 3px solid #fbbf24;
        }

        .sticky-conversion-bar .brand-section {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-shrink: 0;
        }

        .sticky-conversion-bar .logo {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            object-fit: cover;
        }

        .sticky-conversion-bar .brand-name {
            display: flex;
            flex-direction: column;
        }

        .sticky-conversion-bar .brand-name span:first-child {
            font-size: 0.85rem;
            font-weight: 700;
            color: #333;
            line-height: 1.2;
        }

        .sticky-conversion-bar .brand-name span:last-child {
            font-size: 0.7rem;
            color: #666;
            line-height: 1.2;
        }

        .sticky-conversion-bar .btn-group {
            display: flex;
            gap: 8px;
            flex-shrink: 0;
        }

        .sticky-conversion-bar .cta-section {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .sticky-conversion-bar .cta-text {
            font-size: 1rem;
            font-weight: 800;
            color: #fff;
            background: linear-gradient(135deg, #EA580C 0%, #C2410C 100%);
            padding: 10px 18px;
            border-radius: 25px;
            white-space: nowrap;
            box-shadow: 0 4px 0 #9A3412, 0 6px 15px rgba(234, 88, 12, 0.5);
            border: 2px solid rgba(0,0,0,0.1);
            text-decoration: none;
        }

        .sticky-conversion-bar .btn-social {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 52px;
            height: 52px;
            border-radius: 14px;
            text-decoration: none;
            transition: all 0.2s ease;
            border: 3px solid #333;
            background: #fff;
        }

        .sticky-conversion-bar .btn-ig {
            color: #E1306C;
            font-size: 1.6rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .sticky-conversion-bar .btn-ig:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(225, 48, 108, 0.3);
            background: #FFF0F5;
            border-color: #E1306C;
        }

        .sticky-conversion-bar .btn-whatsapp {
            background-color: #fff;
            color: #25D366;
            font-size: 1.7rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            border-color: #25D366;
        }

        .sticky-conversion-bar .btn-whatsapp:hover {
            background-color: #25D366;
            color: #fff;
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4);
        }

        /* 桌面版隱藏 Sticky Bar */
        @media (min-width: 768px) {
            .sticky-conversion-bar {
                display: none !important;
            }
        }

        /* 確保內容區塊底部有 padding 避免被 sticky bar 遮擋 */
        @media (max-width: 767px) {
            footer {
                padding-bottom: 90px !important;
            }
        }

        /* 更小螢幕優化 */
        @media (max-width: 380px) {
            .sticky-conversion-bar .brand-name span:last-child {
                display: none;
            }
            .sticky-conversion-bar .cta-text {
                display: none;
            }
            .sticky-conversion-bar {
                padding: 8px 10px 12px;
            }
        }
'''

# HTML for sticky conversion bar
def get_sticky_bar_html(image_path='image/01_company_logo.png'):
    return f'''
    <!-- Mobile Sticky Conversion Bar -->
    <div class="sticky-conversion-bar" id="sticky-conversion-bar">
        <div class="brand-section">
            <img src="{image_path}" alt="MyO! Logo" class="logo">
            <div class="brand-name">
                <span>MyO!</span>
                <span>myo.makeyourown</span>
            </div>
        </div>
        <div class="cta-section">
            <a href="https://api.whatsapp.com/send?phone=85263796410&text=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E6%88%91%E5%BE%9E%E4%BD%A0%E5%80%91%E7%B6%B2%E7%AB%99%E4%B8%8A%E7%9C%8B%E5%88%B0%E9%80%99%E5%80%8B%E7%94%A2%E5%93%81%EF%BC%81%E6%9C%89%E8%88%88%E8%B6%A3%E4%BA%86%E8%A7%A3%E6%9B%B4%E5%A4%9A%EF%BC%81" target="_blank" class="cta-text">立即查詢</a>
            <div class="btn-group">
                <a href="https://www.instagram.com/myo.makeyourown/" target="_blank" class="btn-social btn-ig" aria-label="Instagram">
                    <i class="fab fa-instagram"></i>
                </a>
                <a href="https://api.whatsapp.com/send?phone=85263796410&text=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E6%88%91%E5%BE%9E%E4%BD%A0%E5%80%91%E7%B6%B2%E7%AB%99%E4%B8%8A%E7%9C%8B%E5%88%B0%E9%80%99%E5%80%8B%E7%94%A2%E5%93%81%EF%BC%81%E6%9C%89%E8%88%88%E8%B6%A3%E4%BA%86%E8%A7%A3%E6%9B%B4%E5%A4%9A%EF%BC%81" target="_blank" class="btn-social btn-whatsapp" aria-label="WhatsApp">
                    <i class="fab fa-whatsapp"></i>
                </a>
            </div>
        </div>
    </div>
'''


def is_blog_file(filepath):
    """Check if the file is in the blog directory"""
    return '/blog/' in filepath


def get_image_path(filepath):
    """Determine the correct image path based on file location"""
    if is_blog_file(filepath):
        return '../image/01_company_logo.png'
    return 'image/01_company_logo.png'


def add_sticky_bar_to_file(filepath):
    """Add sticky bar CSS and HTML to a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if sticky bar already exists
        if 'sticky-conversion-bar' in content:
            print(f'Skipping {filepath} - already has sticky bar')
            return False

        # Add CSS before </style>
        if '</style>' in content:
            content = content.replace('</style>', STICKY_BAR_CSS + '\n    </style>')
        else:
            # Add CSS before </head>
            content = content.replace('</head>', '    <style>' + STICKY_BAR_CSS + '    </style>\n</head>')

        # Add HTML before </body>
        image_path = get_image_path(filepath)
        sticky_bar_html = get_sticky_bar_html(image_path)
        content = content.replace('</body>', sticky_bar_html + '\n</body>')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f'Updated: {filepath}')
        return True

    except Exception as e:
        print(f'Error processing {filepath}: {e}')
        return False


def main():
    """Main function to process all HTML files"""
    base_dir = '/Users/babubu/Documents/GitHub/myo-hk'

    # Files to skip (already have sticky bar or are test files)
    skip_files = [
        'test-runner.html',
        'test-sticky-bar.js',
        'test_file.txt',
        'test2.txt',
        'heic-converter.html'
    ]

    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                # Skip specific files
                if any(skip in file for skip in skip_files):
                    continue
                html_files.append(filepath)

    print(f'Found {len(html_files)} HTML files to process')
    print('-' * 50)

    success_count = 0
    for filepath in html_files:
        if add_sticky_bar_to_file(filepath):
            success_count += 1

    print('-' * 50)
    print(f'Completed! Updated {success_count} out of {len(html_files)} files')


if __name__ == '__main__':
    main()