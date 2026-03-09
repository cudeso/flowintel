# Flowintel user manual

## The Flowintel community

The Flowintel community is built around three concepts: organisations, users and roles. Together they define who can access the platform and what they are allowed to do. You manage all three from the **Community** section in the sidebar, which contains links to **Orgs**, **Users** and **Roles**.

Flowintel does not impose any licence limits on the number of organisations, users or roles you can create. You are free to set up as many as your deployment requires.

Every user must belong to exactly one organisation and must have exactly one role assigned. A user cannot exist without an organisation, and a user cannot hold more than one role at a time.


## Organisations

### Who can manage organisations

You must be logged in and hold the **Admin** system role. Only administrators can create, edit or delete organisations.

### Creating an organisation

Navigate to **Community > Orgs** and click the button to add a new organisation.

You need to provide:

- **Name** (required): the display name of the organisation. Must be unique across the platform.
- **UUID** (optional): a universally unique identifier for the organisation. If you leave this field empty, Flowintel generates one for you automatically. It is recommended to supply your own UUID if you want consistency with external systems.
- **Description** (optional): a free-text description of the organisation.

### Editing an organisation

From the **Community > Orgs** page, locate the organisation you wish to change and click the edit button. You can update the name, UUID or description. Changes take effect straight away.

### Deleting an organisation

You can delete an organisation from the same **Community > Orgs** page. Flowintel will not allow you to delete an organisation if it still has users or if it owns cases. You must first reassign or remove the users and transfer or delete the associated cases before the organisation can be removed.


## Users

### Who can manage users

You must be logged in with sufficient privileges. There are two levels of user management:

- **Admin**: full control over all users across all organisations.
- **Org Admin** (an Editor permission): can create and edit users, but only within their own organisation. An Org Admin cannot assign the Admin system role and cannot move a user to a different organisation.

### Creating a user

Navigate to **Community > Users** and click the button to add a new user.

The following fields are available:

- **First name** (required)
- **Last name** (required)
- **Nickname** (optional)
- **Email** (required): this also serves as the login. The email address must be unique within Flowintel; no two users can share the same email.
- **Matrix ID** (optional): for integration with Matrix messaging.
- **Password** (required): must be between 8 and 64 characters and contain at least one uppercase letter, one lowercase letter and one digit.
- **Confirm password** (required): must match the password.
- **Role** (required): select one of the available roles.
- **Organisation** (required): select the organisation the user belongs to.

Because Flowintel does not send e-mail notifications, the administrator sets the initial password and must share it with the user through a separate, secure channel. There is no self-service signup or automated password distribution.

### Editing a user

From the **Community > Users** page, find the user and click the edit button. You can change any of the fields listed above. If you need to reset the password, tick the **Change password** option and enter the new credentials. Again, communicate the new password through a secure channel outside of Flowintel.

Changes to a user profile take effect immediately. The user does not need to log out and log back in.

### Deleting a user

When you delete a user, Flowintel asks for confirmation first. Once confirmed, the deletion is permanent and cannot be undone.

Note that you cannot delete your own account.


## Roles

### Who can manage roles

You must be logged in with the **Admin** system role. Only administrators can create, edit or delete roles.

### Understanding roles

A role combines a system role type with optional additional permissions. Every role starts with one of three system role types:

| System role | Description |
|---|---|
| **Admin** | Full access to all features and settings. An Admin inherently has all additional permissions. |
| **Read Only** | Can view data but cannot create or modify anything. Cannot have additional permissions. |
| **Editor** | Can create and edit content such as cases and tasks. Additional permissions can be granted to extend what an Editor is allowed to do. |

The three system roles - Admin, Read Only and Editor - are mutually exclusive. You select one per role.

### Additional permissions

When you choose Editor as the system role type, you can grant further permissions from the categories listed below. These permissions have no effect on Admin roles (which already have full access) or Read Only roles (which cannot perform any write actions).

**Organisation Management**

| Permission | Description |
|---|---|
| Org Admin | Allows the user to add, edit or remove users within their own organisation. |

**Privileged Cases**

| Permission | Description |
|---|---|
| Case Admin | Can create and complete cases, and can mark a case as privileged. |
| Queue Admin | Can approve tasks within privileged cases. |
| Queuer | Can request tasks within privileged cases. |

**Audit and Logging**

| Permission | Description |
|---|---|
| Audit Viewer | Allows the user to view history and audit logs. |

**Editor Tools**

| Permission | Description |
|---|---|
| Template Editor | Allows the user to manage case, task or note templates. |
| MISP Editor | Allows the user to manage MISP integration settings. |
| Importer | Allows the user to import data into Flowintel. |

### Creating a role

Navigate to **Community > Roles** and click the button to add a new role.

You need to provide:

- **Name** (required): must be unique.
- **Description** (optional).

Then select the system role type and, if applicable, the additional permissions.

### Editing a role

From the **Community > Roles** page, find the role and click the edit button. You can change the name, description and permissions. Changes to a role take effect immediately for all users who hold that role. Users do not need to log out and log back in.

Note that the three built-in system roles (Admin, Read Only, Editor) cannot be edited or deleted.

### Deleting a role

You can delete a custom role from the **Community > Roles** page. Flowintel will not allow you to delete a role that is currently assigned to one or more users. You must first reassign those users to a different role.


## Your own profile

Your user profile is accessible from the top right of the screen. The navigation bar displays your first and last name together with a coloured badge that gives a quick visual indication of your role: a red shield for Admin, a blue eye for Read Only, or a green pen for Editor. If your Editor role includes additional permissions such as Org Admin or Queue Admin, small icons appear inside the badge as well.

Clicking your name opens a dropdown menu with a link to **My profile**. From there you can view your account details including your name, email, organisation, role and API key.

### Editing your profile

To edit your profile, click the **Edit** button on the profile page. You can change your first name, last name, nickname, Matrix ID and email address. To change your password, tick the **Change password** checkbox and fill in the new password and confirmation fields.

You cannot change your own role or organisation. Only an administrator can do that.

Your API key is shown on the profile page in a blurred state. You can reveal it by clicking the eye icon next to it. If you need a new API key, use the reset button to generate one. The old key is invalidated immediately.

All changes to your profile take effect straight away without needing to log out and log back in.


## Community statistics

Administrators can view statistics about the Flowintel community under **Tools > Stats** on the **Community** tab. This page shows the total number of organisations and users, along with charts for users per organisation, users per role, open cases per organisation and tasks per user.

This tab is only accessible to users with the Admin system role.


## Password reset

Users can change their own password at any time from their profile page. However, if a user forgets their password, they cannot request an automated reset by e-mail. This is by design, for security reasons.

Instead, the password reset process works as follows:

1. The user attempts to log in and enters incorrect credentials.
2. After the failed login attempt, Flowintel shows a link to request a password reset.
3. The user confirms their email address and submits the request.
4. All administrators receive a notification informing them that the user has requested a password reset.
5. An administrator navigates to **Community > Users**, finds the user and manually resets their password.
6. The administrator shares the new password with the user through a separate, secure channel.

Flowintel applies rate limiting to both login attempts and password reset requests to prevent abuse.
