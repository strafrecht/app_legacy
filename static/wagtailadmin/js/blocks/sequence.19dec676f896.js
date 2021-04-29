!function(){"use strict";var e={87862:function(e,n,o){var t=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};n.__esModule=!0;var r=t(o(73609));window.SequenceMember=function(e,n){var o={};o.prefix=n,o.container=r.default("#"+o.prefix+"-container");var t=r.default("#"+o.prefix+"-order");return o.delete=function(){e.deleteMember(o)},o.prependMember=function(n){e.insertMemberBefore(o,n)},o.appendMember=function(n){e.insertMemberAfter(o,n)},o.moveUp=function(){e.moveMemberUp(o)},o.moveDown=function(){e.moveMemberDown(o)},o.markDeleted=function(){r.default("#"+o.prefix+"-deleted").val("1"),o.container.slideUp().dequeue().fadeOut()},o.markAdded=function(){o.container.hide(),o.container.slideDown(),setTimeout((function(){var e=r.default(".input",o.container),n=r.default("input, textarea, [data-hallo-editor], [data-draftail-input]",e).first();n.is("[data-draftail-input]")?n.get(0).draftailEditor.focus():n.trigger("focus")}),250)},o.getIndex=function(){return parseInt(t.val(),10)},o.setIndex=function(e){t.val(e)},o},window.Sequence=function(e){var n={},o=r.default("#"+e.prefix+"-list"),t=r.default("#"+e.prefix+"-count"),a=[];function i(){var o=n.getCount();return t.val(o+1),e.prefix+"-"+o}function l(n){e.onInitializeMember&&e.onInitializeMember(n);var o=n.getIndex();0===o?e.onDisableMoveUp&&e.onDisableMoveUp(n):e.onEnableMoveUp&&e.onEnableMoveUp(n),o===a.length-1?e.onDisableMoveDown&&e.onDisableMoveDown(n):e.onEnableMoveDown&&e.onEnableMoveDown(n),n.markAdded(),a.length>=e.maxNumChildBlocks&&e.onDisableAdd&&e.onDisableAdd(a)}function u(e,n){return r.default(e.replace(/__PREFIX__/g,n).replace(/<-(-*)\/script>/g,"<$1/script>"))}n.getCount=function(){return parseInt(t.val(),10)},n.insertMemberBefore=function(o,t){var r=i(),f=u(t,r);o.container.before(f);for(var s=SequenceMember(n,r),d=o.getIndex(),v=d;v<a.length;v++)a[v].setIndex(v+1);return a.splice(d,0,s),s.setIndex(d),l(s),0===d&&e.onEnableMoveUp&&e.onEnableMoveUp(o),s},n.insertMemberAfter=function(o,t){var r=i(),f=u(t,r);o.container.after(f);for(var s=SequenceMember(n,r),d=o.getIndex()+1,v=d;v<a.length;v++)a[v].setIndex(v+1);return a.splice(d,0,s),s.setIndex(d),l(s),d===a.length-1&&e.onEnableMoveDown&&e.onEnableMoveDown(o),s},n.insertMemberAtStart=function(t){var r=i(),f=u(t,r);o.prepend(f);for(var s=SequenceMember(n,r),d=0;d<a.length;d++)a[d].setIndex(d+1);return a.unshift(s),s.setIndex(0),l(s),a.length>1&&e.onEnableMoveUp&&e.onEnableMoveUp(a[1]),s},n.insertMemberAtEnd=function(t){var r=i(),f=u(t,r);o.append(f);var s=SequenceMember(n,r);return s.setIndex(a.length),a.push(s),l(s),a.length>1&&e.onEnableMoveDown&&e.onEnableMoveDown(a[a.length-2]),s},n.deleteMember=function(n){for(var o=n.getIndex(),t=o+1;t<a.length;t++)a[t].setIndex(t-1);a.splice(o,1),n.markDeleted(),0===o&&a.length>0&&e.onDisableMoveUp&&e.onDisableMoveUp(a[0]),o===a.length&&a.length>0&&e.onDisableMoveDown&&e.onDisableMoveDown(a[a.length-1]),a.length+1>=e.maxNumChildBlocks&&a.length<e.maxNumChildBlocks&&e.onEnableAdd&&e.onEnableAdd(a)},n.moveMemberUp=function(n){var o=n.getIndex();if(o>0){var t=o-1,r=a[t];a[t]=n,n.setIndex(t),a[o]=r,r.setIndex(o),n.container.insertBefore(r.container),0===t&&(e.onDisableMoveUp&&e.onDisableMoveUp(n),e.onEnableMoveUp&&e.onEnableMoveUp(r)),o===a.length-1&&(e.onEnableMoveDown&&e.onEnableMoveDown(n),e.onDisableMoveDown&&e.onDisableMoveDown(r))}},n.moveMemberDown=function(n){var o=n.getIndex();if(o<a.length-1){var t=o+1,r=a[t];a[t]=n,n.setIndex(t),a[o]=r,r.setIndex(o),n.container.insertAfter(r.container),t===a.length-1&&(e.onDisableMoveDown&&e.onDisableMoveDown(n),e.onEnableMoveDown&&e.onEnableMoveDown(r)),0===o&&(e.onEnableMoveUp&&e.onEnableMoveUp(n),e.onDisableMoveUp&&e.onDisableMoveUp(r))}};for(var f=n.getCount(),s=0;s<f;s++){var d=e.prefix+"-"+s,v=SequenceMember(n,d);a[s]=v,e.onInitializeMember&&e.onInitializeMember(v),0===s?e.onDisableMoveUp&&e.onDisableMoveUp(v):e.onEnableMoveUp&&e.onEnableMoveUp(v),s===f-1?e.onDisableMoveDown&&e.onDisableMoveDown(v):e.onEnableMoveDown&&e.onEnableMoveDown(v)}return a.length>=e.maxNumChildBlocks&&e.onDisableAdd&&e.onDisableAdd(a),n}},73609:function(e){e.exports=jQuery}},n={};function o(t){if(n[t])return n[t].exports;var r=n[t]={exports:{}};return e[t].call(r.exports,r,r.exports,o),r.exports}o.m=e,o.x=function(){},o.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),o.o=function(e,n){return Object.prototype.hasOwnProperty.call(e,n)},function(){var e={37:0},n=[[87862,751],[90971,751]],t=function(){},r=function(r,a){for(var i,l,u=a[0],f=a[1],s=a[2],d=a[3],v=0,b=[];v<u.length;v++)l=u[v],o.o(e,l)&&e[l]&&b.push(e[l][0]),e[l]=0;for(i in f)o.o(f,i)&&(o.m[i]=f[i]);for(s&&s(o),r&&r(a);b.length;)b.shift()();return d&&n.push.apply(n,d),t()},a=self.webpackChunkwagtail=self.webpackChunkwagtail||[];function i(){for(var t,r=0;r<n.length;r++){for(var a=n[r],i=!0,l=1;l<a.length;l++){var u=a[l];0!==e[u]&&(i=!1)}i&&(n.splice(r--,1),t=o(o.s=a[0]))}return 0===n.length&&(o.x(),o.x=function(){}),t}a.forEach(r.bind(null,0)),a.push=r.bind(null,a.push.bind(a));var l=o.x;o.x=function(){return o.x=l||function(){},(t=i)()}}(),o.x()}();
//# sourceMappingURL=sequence.js.map