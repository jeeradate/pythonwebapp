"""Main Entry Point for Food Order App.

Sets up NiceGUI Routing, Navigation UI Components, and launches HTTP Server.
Run locally via: python main.py
"""

from pathlib import Path
import sys

from icecream import ic
from nicegui import ui

from food_app.core.config import settings
from food_app.core.database import create_db_and_tables

# Ensure Python discovers package modules in root directory
ROOT_DIR: Path = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def render_header(title: str) -> None:
    """Renders a consistent Top Navigation Header Component across pages.

    Args:
        title (str): Title of the active page view.
    """
    with ui.header().classes(
        "bg-blue-900 text-white flex justify-between items-center px-6 py-3"
    ):
        with (
            ui.row()
            .classes("items-center gap-2 cursor-pointer")
            .on("click", lambda: ui.navigate.to("/"))
        ):
            ui.icon("restaurant", size="32px")
            ui.label("Food Order App").classes("text-xl font-bold")

        ui.label(title).classes("text-lg font-medium")

        with ui.row().classes("gap-4"):
            ui.button("หน้าหลัก", on_click=lambda: ui.navigate.to("/")).props(
                "flat color=white"
            )
            ui.button("ลูกค้า", on_click=lambda: ui.navigate.to("/customer")).props(
                "flat color=white"
            )
            ui.button("ห้องครัว", on_click=lambda: ui.navigate.to("/kitchen")).props(
                "flat color=white"
            )
            ui.button("แคชเชียร์", on_click=lambda: ui.navigate.to("/cashier")).props(
                "flat color=white"
            )
            ui.button("Admin", on_click=lambda: ui.navigate.to("/admin")).props(
                "flat color=white"
            )


# =========================================================
# Page Routes Definitions
# =========================================================


@ui.page("/")
def home_page() -> None:
    """Home view and multi-role dashboard navigation center."""
    render_header("หน้าหลัก (Dashboard)")

    with ui.column().classes("w-full max-w-5xl mx-auto p-6 items-center gap-6"):
        ui.label("🍳 ระบบบริหารจัดการร้านอาหาร (Food Order App)").classes(
            "text-3xl font-bold text-gray-800"
        )
        ui.label("กรุณาเลือกโมดูลการทำงานตามบทบาทผู้ใช้").classes("text-gray-600 mb-4")

        with ui.row().classes("w-full gap-6 justify-center flex-wrap"):
            # Customer Role Card
            with ui.card().classes(
                "w-72 p-6 flex flex-col items-center hover:shadow-lg transition-shadow"
            ):
                ui.icon("qr_code_scanner", size="48px", color="blue-6")
                ui.label("สั่งอาหาร (Customer/POS)").classes("text-lg font-bold mt-2")
                ui.button(
                    "เปิดหน้าสั่งอาหาร",
                    color="blue",
                    on_click=lambda: ui.navigate.to("/customer"),
                ).classes("mt-4 w-full")

            # Kitchen Role Card
            with ui.card().classes(
                "w-72 p-6 flex flex-col items-center hover:shadow-lg transition-shadow"
            ):
                ui.icon("soup_kitchen", size="48px", color="orange-6")
                ui.label("ห้องครัว (KDS)").classes("text-lg font-bold mt-2")
                ui.button(
                    "เปิดหน้าห้องครัว",
                    color="orange",
                    on_click=lambda: ui.navigate.to("/kitchen"),
                ).classes("mt-4 w-full")

            # Cashier Role Card
            with ui.card().classes(
                "w-72 p-6 flex flex-col items-center hover:shadow-lg transition-shadow"
            ):
                ui.icon("payments", size="48px", color="green-6")
                ui.label("แคชเชียร์ (Cashier)").classes("text-lg font-bold mt-2")
                ui.button(
                    "เปิดหน้าคิดเงิน",
                    color="green",
                    on_click=lambda: ui.navigate.to("/cashier"),
                ).classes("mt-4 w-full")

            # Admin Role Card
            with ui.card().classes(
                "w-72 p-6 flex flex-col items-center hover:shadow-lg transition-shadow"
            ):
                ui.icon("settings", size="48px", color="purple-6")
                ui.label("ผู้ดูแลระบบ (Admin)").classes("text-lg font-bold mt-2")
                ui.button(
                    "จัดการ Master Data",
                    color="purple",
                    on_click=lambda: ui.navigate.to("/admin"),
                ).classes("mt-4 w-full")


@ui.page("/customer")
def customer_page() -> None:
    """Customer ordering view placeholder."""
    render_header("หน้าสั่งอาหาร (Customer View)")
    ui.label("🚧 อยู่ระหว่างการพัฒนาโมดูลสั่งอาหาร").classes(
        "text-xl p-8 text-center text-gray-500"
    )


@ui.page("/kitchen")
def kitchen_page() -> None:
    """Kitchen display system view placeholder."""
    render_header("หน้าห้องครัว (Kitchen KDS View)")
    ui.label("🚧 อยู่ระหว่างการพัฒนาโมดูลห้องครัว").classes(
        "text-xl p-8 text-center text-gray-500"
    )


@ui.page("/cashier")
def cashier_page() -> None:
    """Cashier payment view placeholder."""
    render_header("หน้าแคชเชียร์ (Cashier View)")
    ui.label("🚧 อยู่ระหว่างการพัฒนาโมดูลคิดเงิน").classes(
        "text-xl p-8 text-center text-gray-500"
    )


@ui.page("/admin")
def admin_page() -> None:
    """Admin master data view placeholder."""
    render_header("จัดการข้อมูลหลัก (Admin View)")
    ui.label("🚧 อยู่ระหว่างการพัฒนาโมดูล Admin").classes(
        "text-xl p-8 text-center text-gray-500"
    )


# =========================================================
# Application Server Initialization
# =========================================================
def start_app() -> None:
    """Initializes Database tables and launches NiceGUI server instance."""
    create_db_and_tables()
    ic("Starting NiceGUI Server with Config:", settings.HOST, settings.PORT)
    ui.run(
        title=settings.APP_TITLE,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
        favicon="🍳",
    )


if __name__ in {"__main__", "__mp_main__"}:
    start_app()
