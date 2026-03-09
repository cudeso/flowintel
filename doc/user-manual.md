# Flowintel user manual

## What is Flowintel

Flowintel is an open-source case management platform for security analysts and threat intelligence experts. It is developed by [CIRCL](https://www.circl.lu/) and co-funded under the FETTA (Federated European Team for Threat Analysis) project.

Everything in Flowintel centres around **cases** and **tasks**. A case describes a situation that needs to be investigated or handled. Within a case, you create one or more tasks that represent the individual steps of work. Cases and tasks can be enriched with tags, taxonomies and galaxy clusters, which brings the same classification standards used in threat intelligence sharing directly into your case management workflow.

Flowintel also integrates with [MISP](https://www.misp-project.org/) for **sharing findings**. Once a case is complete, you can push it to a MISP instance together with all indicators, notes and objects. From there, MISP's synchronisation features allow you to distribute the case to other teams and communities.

Beyond cases and tasks, Flowintel includes a templating system for repeatable workflows, a calendar view for tracking deadlines, a notification system, analysis modules powered by MISP modules, data export to platforms such as MISP and AIL, and comprehensive audit logging.

![flowintel-Flowintelintro.png](diagrams/flowintel-Flowintelintro.png)

## Follow up on your work

Once you are logged in, Flowintel gives you several ways to keep track of what is happening and what needs your attention. This section covers the home page, notifications and your personal task list.

### The home page

After logging in, you land on the Flowintel home page. At the top, a welcome banner greets you by name and shows three summary badges:

- The number of open cases you have access to, linking directly to the case list.
- The number of tasks assigned to you. If you have tasks waiting, the badge links to your personal task list. If you have none, the badge confirms that no tasks are assigned.
- The number of unread notifications. If there are any, the badge links to the notification page.

Below the welcome banner, the home page displays a list of the ten most recently modified cases. For each case, you can see the case ID and title, a relative timestamp showing when it was last changed, the description (truncated, with an option to expand), the current status, how many tasks are open and closed, the deadline, and any tags, taxonomies or galaxy clusters attached to the case. Private cases only appear here if you belong to an organisation assigned to the case or if you are an administrator.

This list gives you a quick overview of where activity is happening across the cases you have access to, without needing to navigate to the full case list.

### Notifications

Flowintel keeps you informed through in-app notifications. A bell icon in the navigation bar shows the number of unread notifications.

Notifications are created automatically when something relevant happens. The main situations that trigger a notification are:

- You are assigned to a task, or removed from a task.
- A case is completed, revived or deleted.
- A task assigned to you is completed or revived.
- Your organisation is added to a case, removed from a case, or made the owner of a case.
- A deadline on a case or task you are involved in is approaching (within ten days).
- In a privileged case, a task is submitted for approval or a task you requested is approved or rejected.
- A user requests a password reset (sent to administrators).

To view your notifications, click the bell icon. The notification page shows a list of notifications with an icon indicating the type, the message text, and a timestamp showing when it was received or when it was read.

#### Filtering notifications

At the top of the notification page, you can switch between unread and read notifications. A time filter lets you narrow the list to notifications from today, this week, or all time. You can also filter by type, choosing from categories such as Assigned, Unassigned, Completed, Revived, Deleted, Organisation, Deadline and Admin. When a filter is active, a count shows how many notifications match out of the total.

#### Acting on notifications

Each notification can be marked as read or unread by clicking the checkbox next to it. You can also mark all unread notifications as read at once using the button at the top of the list. To remove a notification permanently, click the delete button on that row. Clicking on a notification itself navigates you to the related case.

### Tasks assigned to you

The **Tasks assigned** section in the sidebar takes you to a personal overview of all tasks you are currently assigned to. This page only shows tasks where you are listed as an assigned user.

At the top, a statistics banner summarises your workload: the total number of tasks assigned to you, how many are overdue, and how many are due this week.

Tasks are grouped by the case they belong to. For each task, you can see the title, a relative timestamp of when it was last changed, the description, the current status, tags, the other users assigned, the deadline, and any incomplete subtasks. Deadlines are colour-coded to help you spot urgent items: overdue tasks are highlighted in red, tasks due today or tomorrow in yellow, and tasks further out or without a deadline in grey.

You can switch between ongoing and finished tasks, and sort the list by title, last modification, deadline or status. The sort order can be reversed. The list is paginated, showing twenty tasks per page.


## Cases

Everything in Flowintel starts with a case. A case represents a situation that your team needs to investigate, respond to or track. There is no limit on how many cases Flowintel can store - it depends only on the available system resources.

A case is owned by the organisation of the user who creates it. Other organisations can be assigned to the case later, allowing cross-team collaboration. Within a case, you create tasks to break the work down into individual steps.

Each case is automatically assigned a unique **ID** (the number displayed in front of the case title) and a unique **UUID**. The ID is a simple sequential number used within the Flowintel interface. The UUID is a universally unique identifier that can be used for integration with external systems.

### Creating a case

Navigate to **Cases** in the sidebar and click the plus button to create a new case.

The following fields are available:

- **Title** (required): a short name for the case. Must be unique across all cases in Flowintel.
- **Description** (optional): a free-text field that supports Markdown. Use it to describe the situation, provide background or record initial findings.
- **Deadline date** (optional): the date by which the case should be completed.
- **Deadline time** (optional): a specific time for the deadline. Only applies when a deadline date has been set.
- **Time required** (optional): an estimate of how much effort the case will take, as free text (for example, "2 hours" or "3 days").
- **Ticket ID** (optional): a reference to an external ticketing system. Useful when Flowintel is used alongside another platform.

### Editing a case

From the case detail page, click the edit button. You can change the title, description, deadline, time required, ticket ID, and the private and privileged toggles. Tags, taxonomies and galaxies are edited separately from the same page.

Only users who belong to an organisation assigned to the case can edit it. Administrators can always edit any case. In a privileged case, only an administrator or Case Admin can change the privileged toggle.

### Deleting a case

From the case detail page, click the delete button. Flowintel asks for confirmation before proceeding. Deleting a case removes the case itself, all its tasks, all attached files and the case history. This action cannot be undone.

Only users with the sufficient permissions who belong to an organisation assigned to the case can delete it. In a privileged case, only an administrator or Case Admin can delete the case.

### Behaviour settings

When creating or editing a case, two choices control how the case behaves:

- **Private case**: when enabled, only users whose organisation is assigned to the case can see it. Other users, except administrators, will not find the case in any listing. Use this for sensitive investigations that should not be visible to the entire platform.
- **Privileged case**: when enabled, certain actions on the case require authorisation from a user with elevated permissions. In a privileged case, a user with the Queuer permission cannot directly create tasks in the normal way. Instead, their tasks are created with a Requested status and must be approved by an administrator, Case Admin or Queue Admin before they become active. This implements a four-eye principle where an analyst's work is verified by a supervisor.

In short, a private case controls who can see it, while a privileged case controls who can manage it.

Your Flowintel instance may be configured to enforce privileged mode on every new case automatically. In that situation, the checkbox is ticked for you and cannot be changed.

### Contextual elements

Cases support several types of metadata that help with classification and searching. You can add these when creating a case or edit them afterwards.

- **Taxonomy tags**: tags from MISP taxonomies such as the Traffic Light Protocol (TLP) or the ENISA incident classification. These follow the same standards used in threat intelligence sharing and allow you to label cases consistently.
- **Galaxy clusters**: entries from MISP galaxies, for example a specific threat actor from the Threat Actor galaxy or a technique from the MITRE ATT&CK framework. Attaching galaxy clusters to a case links it to known threats and attack patterns.
- **Custom tags**: tags that are defined locally in your Flowintel instance, independent of any MISP taxonomy. Use these for labels that are specific to your team or organisation.

### Case status

A case has two statuses:

| Status | Meaning |
|---|---|
| **Created** | The case is open and active. This is the initial state when a case is created. |
| **Completed** | The case is finished. It moves out of the active case list and into the finished cases. |

To mark a case as complete, open the case and click the complete button at the top. Flowintel sets the case to **Completed** and records the finish date. A notification is sent to all organisations involved in the case.

To revive a completed case, navigate to finished cases, open the case and click the revive button. This brings the case back to the **Created** status and makes it appear in the active case list again. Note that the tasks are not automatically revived - only the case itself returns to the open state. You can then reopen individual tasks as needed. Reviving is useful when new information surfaces or when additional work is required on a case that was thought to be finished.

In a privileged case, only an administrator or Case Admin can complete or revive the case.

![flowintel-Casemanipulation.png](diagrams/flowintel-Casemanipulation.png)

### Note

A case can have one note written in Markdown. Use it to document findings, analysis or anything relevant to the case as a whole. The note is visible on the case detail page and can be edited at any time.

### Files on a case

You can attach files to a case, for example evidence, logs, exported data or reports. To upload files, go to the case detail page and use the file upload area. You can upload multiple files at once. Each file is stored with its original name and can be downloaded at any time.

To delete a file, click the delete button next to it. The file is removed permanently.

#### Converting a file to a note

If an attached file is a TXT, CSV or JSON file, you can convert it to a note. This reads the content of the file and appends it to the case note. The original file is kept after conversion.

This is particularly useful in day-to-day case management. During an investigation, you often receive data as files - a CSV export from a log management system, a JSON response from an API, or a plain text summary from a colleague. Rather than asking everyone to open and read the file separately, you can convert it to a note, which makes the content directly visible on the case page. This keeps the information accessible without requiring a download and means the key data is part of the case narrative rather than buried in an attachment.

### The case list

Navigating to **Cases** in the sidebar shows you the list of cases you have access to. For each case, the list displays:

- the case ID and title
- whether the case is private or privileged
- the status of the case
- how many tasks are open and how many are completed
- the owner organisation and any other associated organisations
- the deadline
- when the case was last changed
- the tags, taxonomies and galaxies attached to the case

At the top of the list, you have shortcuts to quickly sort by date, title or ID. You can also filter cases by title, tags, taxonomies or galaxies, and further sort by:

- Last modification
- Creation date
- Title
- Deadline
- Status
- My Org

You can reverse the sort order at any time.

By default, the case list shows open cases. A button at the top allows you to switch to finished cases. From the finished cases view, you can switch back to the open cases in the same way.

### Case detail view

Clicking on a case in the list opens its detail page. At the top, you can see when the case was created, when it was last modified, and a summary of tasks showing how many are open and how many are closed.

The detail page also shows the number of files, objects and connectors associated with the case. These features are covered in later sections of this manual.

### Assigning organisations

By default, the case is assigned to the organisation of the user who created it. You can assign additional organisations to the case, which gives their users access to the case and its tasks. This is how you set up collaboration between teams.

A case must always have exactly one owner organisation. You can switch which organisation is the owner, but you cannot remove the owner without assigning a different one first.

### Linked cases

You can link a case to one or more other cases in Flowintel. This is useful when an investigation is an extension of a previous case or when two cases are related. Linked cases appear on the case detail page, allowing you to navigate between them.

### Case history and info

From the case detail page, you can access the case history, which is a full audit log of all actions performed on the case. This shows who did what and when, providing a complete trail for accountability and review.

You can also view the case info, which includes the case's UUID and other metadata.


## Tasks

Tasks are the building blocks of a case. Each task represents a single piece of work that needs to be carried out as part of the investigation or response. A case can contain any number of tasks.

### Creating a task

Open a case and click the button to create a new task.

The following fields are available:

- **Title** (required): a short name for the task.
- **Description** (optional): a free-text field in Markdown. Use it to describe what needs to be done, include instructions or reference external resources.
- **Time required** (optional): an estimate of the effort needed, as free text.
- **Deadline date** (optional): the date by which the task should be finished.
- **Deadline time** (optional): a specific time for the deadline. Only applies when a deadline date has been set.

You can also add taxonomy tags, galaxy clusters and custom tags when creating a task.

### Editing a task

From the task detail view, click the edit button. You can change the title, description, time required, deadline, and the tags, taxonomies and galaxies attached to the task.

Only users who belong to an organisation assigned to the case can edit tasks. In a privileged case, tasks with a Requested or Rejected status can only be edited by an administrator, Case Admin or Queue Admin.

### Deleting a task

From the task detail view, click the delete button. Flowintel asks for confirmation. Deleting a task removes it together with its notes, files, subtasks, URLs and external references. This action cannot be undone.

The same access rules apply as for editing: you must belong to an organisation in the case, and restricted tasks in privileged cases require elevated permissions.

### Contextual elements on tasks

Tasks support the same contextual metadata as cases:

- **Taxonomy tags**: MISP taxonomy tags such as TLP or incident classification.
- **Galaxy clusters**: entries from MISP galaxies such as MITRE ATT&CK techniques or threat actors.
- **Custom tags**: locally defined tags specific to your Flowintel instance.

Adding contextual elements to individual tasks allows you to classify work at a more granular level than the case itself.

### Task status

Each task goes through a set of statuses that track its progress:

| Status | Meaning |
|---|---|
| **Created** | The task has been created but work has not started. |
| **Ongoing** | Work on the task is in progress. |
| **Recurring** | The task repeats and is not expected to be completed once. |
| **Unavailable** | The task cannot be worked on at this time. |
| **Rejected** | The task has been rejected and will not be carried out. |
| **Finished** | The task has been completed. |

In a privileged case, two additional statuses apply to tasks created by users with the Queuer permission:

| Status | Meaning |
|---|---|
| **Requested** | The task has been submitted by a Queuer and is waiting for approval. |
| **Approved** | The task has been approved by an administrator, Case Admin or Queue Admin. |

To change the status of a task, open the task and select a new status from the dropdown. The assigned users are notified when the status changes. In a privileged case, moving a task from Requested to Approved or Rejected triggers a notification to all approvers and assigned users.

To mark a task as finished, you can either set its status to Finished or click the complete button. Completing a task records the finish date and moves the task to the bottom of the task list. To revive a completed task, click the same button again. This sets the task back to the Created status and places it at the end of the open task list.

### Assigning users

A task can be assigned to one or more users. Assigning a user makes it visible in their personal task list, which is accessible from the **Tasks assigned** section in the sidebar.

You can assign yourself to a task by clicking the take button, or assign other users from the assignment panel. To remove an assignment, use the remove button next to the user's name. When a user is assigned by someone else, they receive a notification. Likewise, a user is notified when they are removed from a task.

### Subtasks

Each task can have a set of subtasks. Subtasks are simple checklist items that help you break a task down further. You can add a subtask by entering a short description. Subtasks can be ticked off as they are completed, edited if the description needs changing, reordered to reflect priority, or deleted when they are no longer relevant.

### URLs and tools

You can attach URLs or tool references to a task. This is a free-text list where each entry holds a name or address - for example, a link to an internal wiki page, the name of a forensic tool to use, or a URL to an online service. Entries can be added, edited and deleted from the task detail page.

### Notes

You can add multiple notes to a task in Markdown. Notes are useful for recording findings, decisions or progress updates as work goes on. Each note is stored separately and can be edited or deleted individually.

### Files on a task

You can attach files to a task, for example evidence, screenshots, log extracts or reports. To upload, use the file upload area on the task detail page. You can upload multiple files at once. Files can be downloaded or deleted at any time.

#### Converting a file to a note

As with cases, TXT, CSV and JSON files attached to a task can be converted to a note. On a task, this creates a new note rather than appending to a single note. The original file is kept. See the explanation under Files on a case for why this is useful in practice.

### External references

External references allow you to preserve the content of an external source directly within a task. Where a URL or tool entry is simply a link or a name, an external reference goes further: you provide a URL, and Flowintel can fetch the content of that page and store it as a note on the task.

This is useful for sources that may not remain available indefinitely. If you are referencing a public advisory, a research paper, a blog post or a government notice, there is always a risk that the original page is taken down, moved or changed. By converting the external reference to a note, you preserve the content as it was at the time of retrieval, directly inside your case. The note includes a header showing the source URL and the date it was fetched.

To add an external reference, open the task and enter the URL. You can edit or delete it afterwards. To convert it to a note, click the convert button. Flowintel fetches the page, converts the HTML to Markdown and creates a new note on the task with the content.

![flowintel-Case-task-files-External-references.png](diagrams/flowintel-Case-task-files-External-references.png)

## The Flowintel community

The Flowintel community is built around three concepts: organisations, users and roles. Together they define who can access the platform and what they are allowed to do. You manage all three from the **Community** section in the sidebar, which contains links to **Orgs**, **Users** and **Roles**.

Flowintel does not impose any licence limits on the number of organisations, users or roles you can create. You are free to set up as many as your deployment requires.

Every user must belong to exactly one organisation and must have exactly one role assigned. A user cannot exist without an organisation, and a user cannot hold more than one role at a time.

![flowintel-Flowintel-community.png](diagrams/flowintel-Flowintel-community.png)


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


## Frequently asked questions

**A user has lost their password. What should I do?**

There are two options. If you are an administrator or Org Admin, you can reset the password directly from **Community > Users** by editing the user and ticking **Change password**. Share the new password with the user through a secure channel. Alternatively, ask the user to attempt a login so that Flowintel offers them the option to submit a password reset request. Administrators and Org Admins will then receive a notification and can follow up from there.

**I want users to only be able to consult data, not alter it.**

Assign a role with the **Read Only** system role type to those users. A Read Only user can view cases, tasks and other data but cannot create or modify anything.

**How do I know which users are defined under an organisation?**

Navigate to **Community > Orgs** and click on the organisation. The list of users belonging to that organisation will be displayed, together with their roles.
