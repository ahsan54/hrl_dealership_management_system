# hrl_dealership_management_system

### DMS_Portal
developed the portal for dealership management system, enables individuals to apply for a dealership partnership by providing detailed information, including personal details, contact , location , diff certificates  and investment capacity. Upon submission, system generates  tracking ID for the user to monitor status via portal. portal displays the application state  along with relevant details. Adminis can review applications, approve, or reject them. Upon approval, the system automatically creates a partner record for the approved request.


### Warranty_Card
Developed the Warranty Card Module, that streamlines warranty management. It allows to add warranty duration, on the product form and generate warranty cards for products within sale order lines by clicking the "Add Warranty" button. A wizard opens with pre-filled details, automatically calculating the warranty end date and duration based on the product's form warranty settings. The module first checks if the product is already under an active warranty for the sale order, preventing duplicates. If no active warranty exists, it creates a new warranty with a unique warranty number, linked to the sale order via smart button. On  warranty form, users can select terms and conditions, as well as specify what is included and excluded in the warranty, with a dedicated configuration menu to manage these details. The module generates a PDF warranty card report displaying product information, warranty details, remaining time, and more. Additionally, a hyperlink redirects users to a modern warranty portal where they can view warranty status, remaining time, and other details by entering their warranty number.
Admin can force_expire the card also.
