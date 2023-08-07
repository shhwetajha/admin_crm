from django.urls import path
from order import views
from order.views import *
# from order.views import OrderViewSet, InstallerAvailViewSet, TakeAppointmentViewSet, \
#     InstallerOrderViewSet, GetOrderView, DocumentUploadViewSet, InstallerElectricianOrderViewSet, \
#     InstallerElectricianAvailibilityViewSet, CompanyOrderViewSet, InstallerElectricianAvailibilityListViewSet
from rest_framework.routers import DefaultRouter
from module.views import ModuleView
from batteries.views import BatteryModuleView
from inverters.views import InverterModuleView
from other_component.views import OtherComponentView
from grid_approval.views import DocumentViewSet, GridApprovalView, PresiteRiskViewSet
from installation.views import InstallDocumentUpdateView, WarrantyUpdateView, InstallUpdateView
# from common.views import UpdateUserProfileViewSet,  \
#     GetAdminUserProfileViewSet, GetNonAdminUserProfileViewSet, GetInstallerUserProfileViewSet, \
#     GetTeamUserProfileViewSet, GetUserProfileViewSet, UsersCreateView, \
#         CompanyRegisterView, GetNonAdminUserWithoutApproveProfileViewSet
from call_support.views import CallSupportView, FeedBackView
from common.views import *
# from common.views import CustomerUsersViewSet, UpdateCustomerViewSet, UpdateNoneAdminViewSet, UpdateAdminViewSet, UpdateTeamViewSet, UpdateInstallerViewSet



routers = DefaultRouter()
routers.register('order', OrderViewSet, basename='order')
# routers.register('team-update-order', TeamUpdateOrderViewSet, basename='order')
routers.register('non-admin-order', NonAdminOrderViewSet, basename='company-order')
routers.register('module', ModuleView, basename='module')
routers.register('battery_module', BatteryModuleView, basename='battery_module')
routers.register('inverter_module', InverterModuleView, basename='inverter_module')
routers.register('other_component', OtherComponentView, basename='other_component')
routers.register('upload_meter_docs', DocumentViewSet, basename='upload')
routers.register('update_grid', GridApprovalView, basename='update_grid')
routers.register('update_install_docs', InstallDocumentUpdateView, basename='update_install_docs')
routers.register('update_install_details', InstallUpdateView, basename='update_install_details')
# routers.register('customer', CustomerUsersViewSet, basename='customer')
# routers.register('get_order_list', GetOrderView, basename='get_order_list')
# routers.register('update_customer', UpdateCustomerViewSet, basename='update_customer')
# routers.register('update_none_admin', UpdateNonAdminViewSet, basename='update_none_admin')
# routers.register('update_admin', UpdateAdminViewSet, basename='update_admin')
# routers.register('update_team', UpdateTeamViewSet, basename='update_team')
# routers.register('update_installer', UpdateInstallerViewSet, basename='update_installer')
routers.register('update_profile', UpdateUserProfileViewSet, basename='update_profile')
routers.register('get_admin_profile', GetAdminUserProfileViewSet, basename='get_profile')
routers.register('get_none_admin_profile', GetNonAdminUserProfileViewSet, basename='get_none_admin_profile')
routers.register('comp_profile_without_approve', GetNonAdminUserWithoutApproveProfileViewSet, basename='comp_profile_without_approve')
routers.register('get_installer_profile', GetInstallerUserProfileViewSet, basename='get_installer_profile')
routers.register('get_team_profile', GetTeamUserProfileViewSet, basename='get_team_profile')
routers.register('get_customer_profile', GetCustomerUserProfileViewSet, basename='get_customer_profile')
routers.register('cust-profile', CustomerUserProfileViewSet, basename='cust-profile')
routers.register('update_presite', PresiteRiskViewSet, basename='update_presite')
routers.register('cust-request', CallSupportView, basename='cust-request')
routers.register('cust-review', FeedBackView, basename='cust-review')
routers.register('register', UsersCreateView, basename='register')
routers.register('assign_to', GetUserProfileViewSet, basename='assign_to')
routers.register('assign', InstallerElectricianOrderViewSet, basename='assign')
routers.register('company-register', CompanyRegisterView, basename='company-register')
routers.register('add-availibility', InstallerAvailViewSet, basename='add-availibility')
routers.register('add-holiday', InstallerHolidayViewSet, basename='add-holiday')
routers.register('take-appointment', TakeAppointmentViewSet, basename='take-appointment')
routers.register('get-order', InstallerOrderViewSet, basename='get-order')
routers.register('upload-document', DocumentUploadViewSet, basename='upload-document')
routers.register('update_warranty_docs', WarrantyUpdateView, basename='update_warranty_docs')
routers.register('inst-avail', InstallerElectricianAvailibilityViewSet, basename='inst-avail')
routers.register('inst-avail-list', InstallerElectricianAvailibilityListViewSet, basename='inst-avail-list')
routers.register('company-order', CompanyOrderViewSet, basename='company-order')
routers.register('new-order-list', NewOrderListWithoutAssignView, basename='new-order-list')
routers.register('pending-order-list', AssignedGetOrderView, basename='pending-order-list')
routers.register('completed-order-list', CompletedOrderView, basename='completed-order-list')
routers.register('assign-completed-order-list', InstallerCompletedOrderView, basename='assign-completed-order-list')
# routers.register('invoicing-manager-update-order', InvoicingOrderViewSet, basename='completed-order-list')


urlpatterns = [
    # path("slots_list/", views.slots_list, name="slots_list"),
    # path('home', views.home, name='home'),
]

urlpatterns = routers.urls