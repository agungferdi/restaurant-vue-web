from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io

class OrderPDFService:
    """Service for generating PDF reports from order data"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#F37F0C')  # Primary orange color
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666')
        )
        
        # Normal style for body text
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12
        )
    
    def generate_orders_pdf(self, orders, filename=None):
        """
        Generate a PDF report containing all orders
        
        Args:
            orders: List of order objects with their items
            filename: Optional filename for the PDF
            
        Returns:
            BytesIO buffer containing the PDF data
        """
        # Create a BytesIO buffer to hold the PDF
        buffer = io.BytesIO()
        
        # Create the PDF document
        if filename is None:
            filename = f"orders_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for the PDF elements
        elements = []
        
        # Add title
        title = Paragraph("Restaurant Orders Report", self.title_style)
        elements.append(title)
        
        # Add generation date
        date_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        date_para = Paragraph(date_text, self.subtitle_style)
        elements.append(date_para)
        elements.append(Spacer(1, 20))
        
        # Add summary statistics
        total_orders = len(orders)
        total_revenue = sum(float(order.total_amount or 0) for order in orders)
        pending_orders = len([o for o in orders if o.status == 'pending'])
        completed_orders = len([o for o in orders if o.status == 'completed'])
        cancelled_orders = len([o for o in orders if o.status == 'cancelled'])
        
        summary_data = [
            ['Summary Statistics', ''],
            ['Total Orders', str(total_orders)],
            ['Total Revenue', f"Rp {total_revenue:,.0f}"],
            ['Pending Orders', str(pending_orders)],
            ['Completed Orders', str(completed_orders)],
            ['Cancelled Orders', str(cancelled_orders)]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F37F0C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 30))
        
        # Add orders table
        if orders:
            # Orders header
            orders_title = Paragraph("Order Details", self.styles['Heading2'])
            elements.append(orders_title)
            elements.append(Spacer(1, 10))
            
            # Create table data
            table_data = [
                ['Order ID', 'Customer', 'Status', 'Items', 'Total', 'Date']
            ]
            
            for order in orders:
                # Format order items
                items_text = []
                for item in order.order_items:
                    items_text.append(f"{item.menu.name} (x{item.quantity})")
                items_str = "\n".join(items_text) if items_text else "No items"
                
                # Format date
                date_str = order.created_at.strftime('%m/%d/%Y') if order.created_at else ''
                
                # Status styling
                status_display = order.status.title()
                
                table_data.append([
                    str(order.id),
                    order.customer_name,
                    status_display,
                    items_str,
                    f"Rp {float(order.total_amount or 0):,.0f}",
                    date_str
                ])
            
            # Create and style the table
            orders_table = Table(table_data, colWidths=[0.7*inch, 1.5*inch, 1*inch, 2.5*inch, 1*inch, 1*inch])
            orders_table.setStyle(TableStyle([
                # Header styling
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F37F0C')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                
                # Data rows styling
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                
                # Alternate row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            elements.append(orders_table)
        else:
            no_orders = Paragraph("No orders found.", self.body_style)
            elements.append(no_orders)
        
        # Add footer
        elements.append(Spacer(1, 30))
        footer_text = "This report was automatically generated by the Restaurant Management System."
        footer = Paragraph(footer_text, ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        ))
        elements.append(footer)
        
        # Build the PDF
        doc.build(elements)
        
        # Get the value of the BytesIO buffer
        buffer.seek(0)
        return buffer
    
    def generate_single_order_pdf(self, order, filename=None):
        """
        Generate a PDF for a single order (useful for receipts)
        
        Args:
            order: Single order object with items
            filename: Optional filename for the PDF
            
        Returns:
            BytesIO buffer containing the PDF data
        """
        buffer = io.BytesIO()
        
        if filename is None:
            filename = f"order_{order.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        elements = []
        
        # Title
        title = Paragraph(f"Order Receipt #{order.id}", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Order info
        order_info = [
            ['Customer:', order.customer_name],
            ['Order Date:', order.created_at.strftime('%B %d, %Y at %I:%M %p') if order.created_at else ''],
            ['Status:', order.status.title()],
            ['Notes:', order.notes or 'None']
        ]
        
        info_table = Table(order_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        # Order items
        items_title = Paragraph("Order Items", self.styles['Heading3'])
        elements.append(items_title)
        elements.append(Spacer(1, 10))
        
        items_data = [['Item', 'Quantity', 'Price', 'Subtotal']]
        
        for item in order.order_items:
            price = float(item.menu.price)
            subtotal = price * item.quantity
            items_data.append([
                item.menu.name,
                str(item.quantity),
                f"Rp {price:,.0f}",
                f"Rp {subtotal:,.0f}"
            ])
        
        # Add total row
        items_data.append(['', '', 'Total:', f"Rp {float(order.total_amount or 0):,.0f}"])
        
        items_table = Table(items_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F37F0C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        
        elements.append(items_table)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer