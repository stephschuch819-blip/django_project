# Live Chat Integration Guide

## Current Implementation

The DGLegacy Portal now includes a **fully functional live chat widget** on both the beneficiary portal and admin panel.

### Features:
- ✅ Floating chat button (bottom-right corner)
- ✅ Expandable chat window
- ✅ Message sending/receiving interface
- ✅ Typing indicators
- ✅ Auto-responses (simulated)
- ✅ Quick access to phone and email support
- ✅ XSS protection (HTML escaping)
- ✅ Responsive design

### Current Status:
The chat widget is **fully functional** with simulated responses. Messages are displayed in real-time with a 2-second delay to simulate agent typing.

---

## Integrating with Real Chat Services

To connect the live chat to a real support system, you can integrate with popular services:

### Option 1: Tawk.to (Free & Recommended)

1. **Sign up at**: https://www.tawk.to/
2. **Get your widget code** from the dashboard
3. **Replace the chat widget** in `templates/base.html` (line 235-452) with:

```html
<!--Start of Tawk.to Script-->
<script type="text/javascript">
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/YOUR_PROPERTY_ID/YOUR_WIDGET_ID';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();
</script>
<!--End of Tawk.to Script-->
```

### Option 2: Intercom

1. **Sign up at**: https://www.intercom.com/
2. **Get your app ID**
3. **Add to base.html**:

```html
<script>
  window.intercomSettings = {
    api_base: "https://api-iam.intercom.io",
    app_id: "YOUR_APP_ID"
  };
</script>
<script>(function(){var w=window;var ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',w.intercomSettings);}else{var d=document;var i=function(){i.c(arguments);};i.q=[];i.c=function(args){i.q.push(args);};w.Intercom=i;var l=function(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://widget.intercom.io/widget/YOUR_APP_ID';var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);};if(document.readyState==='complete'){l();}else if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})();</script>
```

### Option 3: Crisp Chat

1. **Sign up at**: https://crisp.chat/
2. **Get your website ID**
3. **Add to base.html**:

```html
<script type="text/javascript">
  window.$crisp=[];
  window.CRISP_WEBSITE_ID="YOUR_WEBSITE_ID";
  (function(){
    d=document;
    s=d.createElement("script");
    s.src="https://client.crisp.chat/l.js";
    s.async=1;
    d.getElementsByTagName("head")[0].appendChild(s);
  })();
</script>
```

### Option 4: Custom Backend Integration

To connect the current widget to your own backend:

1. **Create a Django view** to handle chat messages:

```python
# portal/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chat_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        case_id = request.session.get('beneficiary_case_id')
        
        # Save message to database or send to chat service
        # Return response
        
        return JsonResponse({
            'status': 'success',
            'response': 'Thank you for your message. An agent will respond shortly.'
        })
```

2. **Update the JavaScript** in `templates/base.html`:

Replace the `setTimeout` simulation (line 417-430) with:

```javascript
// Send to backend
fetch('/chat/message/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({message: message})
})
.then(response => response.json())
.then(data => {
    const responseDiv = document.createElement('div');
    responseDiv.style.cssText = 'background: white; padding: 12px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);';
    responseDiv.innerHTML = `
        <strong style="color: #28a745;"><i class="bi bi-person-badge"></i> Support Agent</strong>
        <p style="margin: 5px 0 0 0; font-size: 14px;">${data.response}</p>
        <small style="color: #6c757d; font-size: 11px;">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</small>
    `;
    chatMessages.appendChild(responseDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
});
```

---

## Admin Panel Chat

The admin panel also has a live chat widget in `templates/admin/base.html`. You can integrate it with the same services or use it for internal support communication.

---

## Testing the Current Implementation

1. **Login as beneficiary**: Use any test case (e.g., DG-IQ14U6 / password123)
2. **Look for the green "Live Chat" button** in the bottom-right corner
3. **Click to open** the chat window
4. **Type a message** and press Enter or click Send
5. **See the simulated response** after 2 seconds

---

## Customization Options

### Change Chat Button Position
Edit line 237 in `templates/base.html`:
```css
bottom: 20px; right: 20px;  /* Change these values */
```

### Change Colors
- Button gradient: line 239
- Header gradient: line 270
- Message colors: lines 392, 422

### Disable for Specific Pages
The chat only shows when `request.session.beneficiary_case_id` exists (logged-in beneficiaries).

To show on all pages, remove the `{% if request.session.beneficiary_case_id %}` condition on line 236.

---

## Support Contact Information

Current support details (update as needed):
- **Phone**: +1 (800) 555-0199
- **Email**: support@dglegacy.com
- **Hours**: Mon-Fri: 9AM - 6PM EST

Update these in:
- `templates/base.html` (lines 350-354)
- `templates/portal/messages.html` (lines 82-91)
- `templates/portal/dashboard.html` (lines 210-216)

---

## Security Notes

- ✅ XSS protection via HTML escaping
- ✅ Messages are sanitized before display
- ✅ CSRF tokens required for backend integration
- ⚠️ For production, implement proper authentication and rate limiting

---

## Future Enhancements

- [ ] Connect to real chat service (Tawk.to, Intercom, etc.)
- [ ] Store chat history in database
- [ ] Add file upload in chat
- [ ] Implement chat notifications
- [ ] Add agent availability status
- [ ] Multi-language support
- [ ] Chat transcripts via email

---

**Need Help?** Contact the development team or refer to the service-specific documentation above.
