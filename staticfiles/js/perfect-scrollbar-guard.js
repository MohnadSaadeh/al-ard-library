// Guard wrapper for PerfectScrollbar: ensure constructor never throws when element is falsy.
(function(){
    if (typeof window === 'undefined') return;
    if (!window.PerfectScrollbar) return;

    var OriginalPS = window.PerfectScrollbar;

    // keep a single quiet log to avoid spamming the console if theme calls init many times
    var _psGuardLogged = false;
    function GuardedPerfectScrollbar(el, options) {
        if (!el) {
            if (!_psGuardLogged) {
                if (console && console.debug) console.debug('PerfectScrollbar init skipped: no element provided');
                _psGuardLogged = true;
            }
            // Return a lightweight stub with common methods used by themes to avoid further errors
            return {
                destroy: function(){},
                element: null
            };
        }
        return new OriginalPS(el, options);
    }

    // Preserve prototype so instanceof checks and methods work for real instances
    GuardedPerfectScrollbar.prototype = OriginalPS.prototype;

    // Replace global
    window.PerfectScrollbar = GuardedPerfectScrollbar;
})();
